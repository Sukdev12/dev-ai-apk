import os
import sys
import time
import json
import base64
import subprocess
import threading
import urllib.request
from datetime import datetime

# ===== CONFIG =====
API_KEY = os.getenv("GEMINI_API_KEY", "")

# ===== FAST VOICE =====
def speak(text):
    """Fast voice output."""
    print(f"🤖 Dev: {text}")
    os.system(f'termux-tts-speak "{text}" 2>/dev/null &')

def listen_voice(timeout=4):
    """Quick voice capture with timeout."""
    try:
        output = subprocess.check_output(
            ["termux-speech-to-text"],
            timeout=timeout
        ).decode("utf-8").strip()
        return output.lower() if output else None
    except subprocess.TimeoutExpired:
        return None
    except:
        return None

# ===== FAST EXECUTION =====
def exec_cmd(cmd):
    """Execute command instantly."""
    os.system(f'rish -c "{cmd}" 2>/dev/null &')

# ===== APP MAP =====
APPS = {
    "youtube": "com.google.android.youtube",
    "whatsapp": "com.whatsapp",
    "prisma": "com.prisma3D.prisma3D",
    "alight": "com.alightcreative.motion",
    "instagram": "com.instagram.android",
    "chrome": "com.android.chrome",
    "flipaclip": "com.vblast.flipaclip",
    "settings": "com.android.settings",
    "gallery": "com.android.gallery3d",
    "photos": "com.google.android.apps.photos",
    "maps": "com.google.android.apps.maps",
    "calculator": "com.android.calculator2",
    "clock": "com.android.deskclock",
    "calendar": "com.android.calendar"
}

# ===== COMMAND PROCESSOR =====
def process_command(command):
    """Process command fast."""
    command = command.lower().strip()
    print(f"⚡ Command: {command}")
    
    # Exit commands
    if command in ["stop", "exit", "quit", "shutdown"]:
        speak("Goodbye boss!")
        return "exit"
    
    # Open app
    if "open" in command:
        for name, package in APPS.items():
            if name in command:
                exec_cmd(f"monkey -p {package} 1")
                speak(f"Opening {name}")
                return "done"
    
    # System commands
    if "home" in command or "go home" in command:
        exec_cmd("input keyevent 3")
        speak("Going home")
        return "done"
    
    if "back" in command or "go back" in command:
        exec_cmd("input keyevent 4")
        speak("Going back")
        return "done"
    
    if "screenshot" in command:
        exec_cmd("screencap -p /sdcard/screenshot.png")
        speak("Screenshot taken")
        return "done"
    
    # Tap commands
    if "tap" in command:
        if "top" in command:
            exec_cmd("input tap 540 200")
        elif "bottom" in command:
            exec_cmd("input tap 540 1800")
        elif "left" in command:
            exec_cmd("input tap 200 960")
        elif "right" in command:
            exec_cmd("input tap 880 960")
        else:
            exec_cmd("input tap 540 960")
        speak("Tapped")
        return "done"
    
    # Swipe commands
    if "swipe" in command or "scroll" in command:
        if "up" in command:
            exec_cmd("input swipe 540 1600 540 400 200")
        elif "down" in command:
            exec_cmd("input swipe 540 400 540 1600 200")
        else:
            exec_cmd("input swipe 540 1200 540 600 200")
        speak("Swiped")
        return "done"
    
    # Build commands
    if "build" in command or "create" in command or "make" in command:
        if "website" in command:
            speak("Building website...")
            build_website(command)
            return "done"
        elif "app" in command:
            speak("Building app...")
            build_app(command)
            return "done"
        elif "game" in command:
            speak("Building game...")
            build_game(command)
            return "done"
    
    # Default
    speak("Done boss!")
    return "done"

# ===== BUILD FUNCTIONS =====
def build_website(command):
    """Generate website."""
    description = command.replace("build", "").replace("website", "").replace("create", "").replace("make", "").strip()
    
    if not API_KEY:
        speak("No API key for generation")
        return
    
    prompt = f"Create complete HTML/CSS/JS for: {description}. Include modern design, responsive."
    
    try:
        response = call_gemini(prompt)
        if response:
            with open("index.html", "w") as f:
                f.write(response)
            speak("Website created! File: index.html")
        else:
            speak("Failed to generate")
    except:
        speak("Error generating website")

def build_app(command):
    """Generate app."""
    description = command.replace("build", "").replace("app", "").replace("create", "").replace("make", "").strip()
    
    if not API_KEY:
        speak("No API key for generation")
        return
    
    prompt = f"Create complete Python Flask web app for: {description}"
    
    try:
        response = call_gemini(prompt)
        if response:
            with open("app.py", "w") as f:
                f.write(response)
            speak("App created! File: app.py")
        else:
            speak("Failed to generate")
    except:
        speak("Error generating app")

def build_game(command):
    """Generate game."""
    description = command.replace("build", "").replace("game", "").replace("create", "").replace("make", "").strip()
    
    if not API_KEY:
        speak("No API key for generation")
        return
    
    prompt = f"Create complete HTML game with JavaScript for: {description}"
    
    try:
        response = call_gemini(prompt)
        if response:
            with open("game.html", "w") as f:
                f.write(response)
            speak("Game created! File: game.html")
        else:
            speak("Failed to generate")
    except:
        speak("Error generating game")

def call_gemini(prompt):
    """Call Gemini API."""
    if not API_KEY:
        return None
    
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    try:
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result['candidates'][0]['content']['parts'][0]['text']
    except:
        return None

# ===== MAIN LOOP =====
def main():
    speak("Dev AI ready!")
    print("\n" + "="*50)
    print("🚀 DEV FAST VOICE ASSISTANT")
    print("Always listening... Just say your command")
    print("Examples: 'Open YouTube', 'Go home', 'Screenshot'")
    print("Say 'stop' or 'exit' to quit")
    print("="*50 + "\n")
    
    while True:
        try:
            # Listen for command
            command = listen_voice(4)
            
            if command:
                result = process_command(command)
                if result == "exit":
                    break
            
        except KeyboardInterrupt:
            speak("Goodbye boss!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main()
