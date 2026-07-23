import os
import sys
import time
import json
import base64
import urllib.request
import subprocess
import threading
import queue

API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-3.5-flash-lite"

def speak(text):
    """Voice output feedback."""
    print(f"🤖 Dev: {text}")
    os.system(f'termux-tts-speak "{text}"')

def exec_shell(cmd):
    """Executes system input commands via Shizuku (rish)."""
    os.system(f'rish -c "{cmd}" 2>/dev/null')

def listen_voice_with_timeout(timeout=5):
    """Listen for voice with timeout to prevent blocking."""
    print("\n🎙️ Listening... (say something within 5 seconds)")
    
    try:
        # Use timeout with subprocess
        output = subprocess.check_output(
            ["termux-speech-to-text"], 
            timeout=timeout
        ).decode("utf-8").strip()
        
        if output:
            print(f"🗣️ You said: {output}")
            return output.lower()
    except subprocess.TimeoutExpired:
        print("⏰ No voice detected, continuing...")
        return None
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None
    
    return None

def listen_wake_word():
    """Listen specifically for wake words."""
    print("\n🎙️ Waiting for wake word... (say 'Dev' or 'Hey Dev')")
    
    try:
        output = subprocess.check_output(
            ["termux-speech-to-text"], 
            timeout=3
        ).decode("utf-8").strip()
        
        if output:
            output_lower = output.lower()
            print(f"🗣️ Heard: {output}")
            
            # Check for wake words
            wake_words = ["dev", "hey dev", "hello dev", "hi dev"]
            if any(w in output_lower for w in wake_words):
                return True, output_lower
            return False, output_lower
    except subprocess.TimeoutExpired:
        pass
    except Exception:
        pass
    
    return False, None

def process_command(command):
    """Process user command."""
    print(f"📱 Processing: {command}")
    
    # Open apps
    if "open" in command:
        app_map = {
            "flipaclip": "com.vblast.flipaclip",
            "alight": "com.alightcreative.motion",
            "prisma": "com.prisma3d.app",
            "settings": "com.android.settings",
            "youtube": "com.google.android.youtube",
            "chrome": "com.android.chrome",
            "instagram": "com.instagram.android"
        }
        for app_name, package in app_map.items():
            if app_name in command:
                exec_shell(f"am start -n {package}/.MainActivity")
                speak(f"Opening {app_name}")
                return
    
    # Home button
    if "home" in command or "back" in command:
        if "home" in command:
            exec_shell("input keyevent 3")
            speak("Going home")
            return
        elif "back" in command:
            exec_shell("input keyevent 4")
            speak("Going back")
            return
    
    # Tap command example
    if "tap" in command or "click" in command:
        exec_shell("input tap 500 1000")
        speak("Tapped")
        return
    
    # Screenshot
    if "screenshot" in command or "capture" in command:
        exec_shell("screencap -p /sdcard/screenshot.png")
        speak("Screenshot taken")
        return
    
    # Default response
    speak("Command received boss!")

def main():
    speak("Yes boss! Dev AI is ready.")
    
    while True:
        # Listen for wake word
        woke, command = listen_wake_word()
        
        if woke:
            speak("Listening boss!")
            
            # Listen for actual command
            for attempt in range(3):  # Try 3 times
                cmd = listen_voice_with_timeout(5)
                if cmd:
                    process_command(cmd)
                    break
                else:
                    if attempt < 2:
                        speak("Please say your command")
                    else:
                        speak("No command heard boss")
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
