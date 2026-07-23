import os
import sys
import time
import json
import subprocess

def speak(text):
    """Voice output."""
    print(f"🤖 Dev: {text}")
    os.system(f'termux-tts-speak "{text}"')

def exec_shell(cmd):
    """Execute command via Shizuku."""
    result = os.system(f'rish -c "{cmd}" 2>/dev/null')
    return result == 0

def process_command(command):
    """Process text commands."""
    command = command.lower().strip()
    print(f"📱 Processing: {command}")
    
    # ===== APP CONTROLS =====
    apps = {
        "flipaclip": "com.vblast.flipaclip",
        "alight": "com.alightcreative.motion",
        "prisma": "com.prisma3d.app",
        "settings": "com.android.settings",
        "youtube": "com.google.android.youtube",
        "chrome": "com.android.chrome",
        "whatsapp": "com.whatsapp",
        "instagram": "com.instagram.android",
        "twitter": "com.twitter.android",
        "gallery": "com.android.gallery3d"
    }
    
    for name, package in apps.items():
        if name in command:
            exec_shell(f"am start -n {package}/.MainActivity")
            speak(f"Opening {name}")
            return True
    
    # ===== SYSTEM COMMANDS =====
    if "home" in command:
        exec_shell("input keyevent 3")
        speak("Going home")
        return True
    
    if "back" in command:
        exec_shell("input keyevent 4")
        speak("Going back")
        return True
    
    if "recent" in command:
        exec_shell("input keyevent 187")
        speak("Showing recent apps")
        return True
    
    # ===== SCREENSHOT =====
    if "screenshot" in command or "capture" in command:
        exec_shell("screencap -p /sdcard/screenshot.png")
        speak("Screenshot saved")
        return True
    
    # ===== TAP COMMANDS =====
    if "tap" in command:
        # Default tap at center
        exec_shell("input tap 540 960")
        speak("Tapped center")
        return True
    
    if "top" in command:
        exec_shell("input tap 540 200")
        speak("Tapped top")
        return True
    
    if "bottom" in command:
        exec_shell("input tap 540 1800")
        speak("Tapped bottom")
        return True
    
    # ===== SWIPE COMMANDS =====
    if "swipe up" in command:
        exec_shell("input swipe 540 1600 540 400 300")
        speak("Swiping up")
        return True
    
    if "swipe down" in command:
        exec_shell("input swipe 540 400 540 1600 300")
        speak("Swiping down")
        return True
    
    if "scroll" in command:
        exec_shell("input swipe 540 1200 540 600 200")
        speak("Scrolling")
        return True
    
    # ===== TYPE COMMAND =====
    if "type" in command:
        text = command.replace("type", "").strip()
        if text:
            formatted = text.replace(" ", "%s")
            exec_shell(f"input text {formatted}")
            speak(f"Typed: {text}")
        return True
    
    # ===== DEVICE INFO =====
    if "info" in command or "status" in command:
        exec_shell("dumpsys battery")
        speak("Device info displayed")
        return True
    
    # ===== DEFAULT =====
    speak("Command not recognized boss!")
    return False

def main():
    speak("Yes boss! Dev AI is ready.")
    print("\n" + "="*50)
    print("🤖 DEV AI ASSISTANT - TEXT MODE")
    print("Type your commands below")
    print("Examples: 'Open YouTube', 'Go home', 'Screenshot'")
    print("Type 'exit' or 'quit' to stop")
    print("="*50 + "\n")
    
    while True:
        try:
            # Get text input
            command = input("🧑 You: ").strip()
            
            if command.lower() in ["exit", "quit", "stop"]:
                speak("Shutting down boss!")
                break
            
            if command:
                process_command(command)
                
        except KeyboardInterrupt:
            speak("Shutting down boss!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            speak("Error occurred boss")

if __name__ == "__main__":
    main()
