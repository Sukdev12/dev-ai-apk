import os
import sys
import time
import json
import base64
import urllib.request
import subprocess

API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-3.5-flash-lite"

def speak(text):
    """Voice output feedback."""
    print(f"🤖 Dev: {text}")
    os.system(f'termux-tts-speak "{text}"')

def exec_shell(cmd):
    """Executes system input commands via Shizuku (rish)."""
    os.system(f'rish -c "{cmd}" 2>/dev/null')

def listen_voice():
    """Listen for voice command using Termux native."""
    print("\n🎙️ Listening for command...")
    try:
        output = subprocess.check_output(["termux-speech-to-text"]).decode("utf-8").strip()
        if output:
            print(f"🗣️ You said: {output}")
            return output.lower()
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None
    return None

def process_command(command):
    """Process user command."""
    print(f"📱 Processing: {command}")
    
    # Open apps
    if "open" in command:
        app_map = {
            "flipaclip": "com.vblast.flipaclip",
            "alight": "com.alightcreative.motion",
            "prisma": "com.prisma3d.app",
            "settings": "com.android.settings"
        }
        for app_name, package in app_map.items():
            if app_name in command:
                exec_shell(f"am start -n {package}/.MainActivity")
                speak(f"Opening {app_name}")
                return
    
    # Home button
    if "home" in command or "go back" in command:
        exec_shell("input keyevent 3")
        speak("Going home")
        return
    
    # Generic response
    speak("Command received boss!")

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
