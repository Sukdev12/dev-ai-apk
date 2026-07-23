import os
import sys
import time
import json
import base64
import urllib.request
import subprocess
import speech_recognition as sr

API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-3.5-flash-lite"

def speak(text):
    """Voice output feedback."""
    print(f"🤖 Dev: {text}")
    os.system(f'termux-tts-speak "{text}"')

def exec_shell(cmd):
    """Executes system input commands via Shizuku (rish)."""
    os.system(f'rish -c "{cmd}" 2>/dev/null')

class DevVisionEngine:
    def capture_screen(self, path="screen.jpg"):
        exec_shell(f"screencap -p /sdcard/{path}")
        exec_shell(f"mv /sdcard/{path} ./")
        return path

    def tap(self, x, y):
        exec_shell(f"input tap {x} {y}")

    def swipe(self, x1, y1, x2, y2, duration=500):
        exec_shell(f"input swipe {x1} {y1} {x2} {y2} {duration}")

    def type_text(self, text):
        formatted = text.replace(" ", "%s")
        exec_shell(f"input text {formatted}")

vision = DevVisionEngine()

def listen_voice():
    """Listen for voice command using SpeechRecognition."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text.lower()
        except:
            return None

def ask_gemini(prompt, image_path=None):
    """Query Gemini API directly."""
    headers = {"Content-Type": "application/json", "x-goog-api-key": API_KEY}
    parts = [{"text": prompt}]
    
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode("utf-8")
            parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": img_b64
                }
            })
    
    payload = json.dumps({"contents": [{"parts": parts}]}).encode("utf-8")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"
    
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            return res['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error: {e}"

def process_command(command):
    """Process user command."""
    if "open" in command:
        app_map = {
            "flipaclip": "com.vblast.flipaclip",
            "alight motion": "com.alightcreative.motion",
            "prisma": "com.prisma3d.app"
        }
        for app_name, package in app_map.items():
            if app_name in command:
                exec_shell(f"am start -n {package}/.MainActivity")
                speak(f"Opening {app_name}")
                return
    
    if "tap" in command:
        speak("Where should I tap?")
        vision.tap(500, 1000)  # Example coordinates
    
    if "home" in command:
        exec_shell("input keyevent 3")
        speak("Going home")
    
    speak("Task completed boss!")

def main():
    speak("Yes boss! Dev AI is ready.")
    while True:
        cmd = listen_voice()
        if cmd:
            if "stop" in cmd or "exit" in cmd:
                speak("Shutting down boss!")
                break
            if "dev" in cmd or "hey" in cmd:
                speak("Listening boss!")
                process_command(cmd)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
