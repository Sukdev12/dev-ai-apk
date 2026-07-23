import os
import sys
import time
import subprocess
import threading

def speak(text):
    """Voice output."""
    print(f"🤖 Dev: {text}")
    os.system(f'termux-tts-speak "{text}" 2>/dev/null &')

def listen_once():
    """Listen for one command when triggered."""
    print("\n🎙️ Speak now... (say your command)")
    try:
        output = subprocess.check_output(
            ["termux-speech-to-text"],
            timeout=5
        ).decode("utf-8").strip()
        if output:
            print(f"🗣️ You said: {output}")
            return output.lower()
    except subprocess.TimeoutExpired:
        print("⏰ No input detected")
    except Exception as e:
        print(f"❌ Error: {e}")
    return None

def exec_cmd(cmd):
    """Execute command."""
    os.system(f'rish -c "{cmd}" 2>/dev/null &')

APPS = {
    "youtube": "com.google.android.youtube",
    "whatsapp": "com.whatsapp",
    "prisma": "com.prisma3D.prisma3D",
    "alight": "com.alightcreative.motion",
    "instagram": "com.instagram.android",
    "chrome": "com.android.chrome",
    "flipaclip": "com.vblast.flipaclip",
    "settings": "com.android.settings"
}

def process_command(command):
    """Process command."""
    command = command.lower().strip()
    print(f"⚡ Processing: {command}")
    
    if command in ["stop", "exit", "quit"]:
        speak("Goodbye boss!")
        return "exit"
    
    # Open apps
    if "open" in command:
        for name, package in APPS.items():
            if name in command:
                exec_cmd(f"monkey -p {package} 1")
                speak(f"Opening {name}")
                return "done"
    
    # System commands
    if "home" in command:
        exec_cmd("input keyevent 3")
        speak("Going home")
        return "done"
    
    if "back" in command:
        exec_cmd("input keyevent 4")
        speak("Going back")
        return "done"
    
    if "screenshot" in command:
        exec_cmd("screencap -p /sdcard/screenshot.png")
        speak("Screenshot taken")
        return "done"
    
    if "tap" in command:
        exec_cmd("input tap 540 960")
        speak("Tapped")
        return "done"
    
    if "swipe" in command or "scroll" in command:
        if "up" in command:
            exec_cmd("input swipe 540 1600 540 400 200")
        else:
            exec_cmd("input swipe 540 400 540 1600 200")
        speak("Swiped")
        return "done"
    
    speak("Done boss!")
    return "done"

def main():
    speak("Dev AI ready!")
    print("\n" + "="*50)
    print("🚀 DEV MANUAL VOICE ASSISTANT")
    print("Type 'v' and press Enter to speak a command")
    print("Or type commands directly:")
    print("  - 'open youtube'")
    print("  - 'home'")
    print("  - 'screenshot'")
    print("  - 'exit' to quit")
    print("="*50 + "\n")
    
    while True:
        try:
            user_input = input("🧑 > ").strip().lower()
            
            if user_input == "v":
                # Voice mode
                command = listen_once()
                if command:
                    result = process_command(command)
                    if result == "exit":
                        break
            elif user_input:
                # Text mode
                result = process_command(user_input)
                if result == "exit":
                    break
                    
        except KeyboardInterrupt:
            speak("Goodbye boss!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
