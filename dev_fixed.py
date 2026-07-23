import os
import sys
import time
import subprocess
import threading

def speak_async(text):
    """Speak without blocking."""
    def _speak():
        os.system(f'termux-tts-speak "{text}" 2>/dev/null')
    threading.Thread(target=_speak, daemon=True).start()

def exec_shell(cmd):
    """Execute command via Shizuku."""
    try:
        result = os.system(f'rish -c "{cmd}" 2>/dev/null')
        return result == 0
    except:
        return False

# CORRECT PACKAGE NAMES FROM YOUR SYSTEM
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

def open_app(app_name):
    """Open app using correct package."""
    app_name = app_name.lower().strip()
    
    # Find package
    package = None
    for name, pkg in APPS.items():
        if name in app_name:
            package = pkg
            break
    
    if not package:
        speak_async(f"App {app_name} not found")
        return False
    
    print(f"📱 Opening: {app_name} ({package})")
    
    # Try multiple methods
    methods = [
        f'monkey -p {package} 1',
        f'am start -n {package}/.MainActivity',
        f'am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n {package}'
    ]
    
    for method in methods:
        print(f"🔧 Trying: {method}")
        if exec_shell(method):
            speak_async(f"Opening {app_name}")
            return True
    
    speak_async(f"Failed to open {app_name}")
    return False

def process_command(command):
    """Process command."""
    command = command.lower().strip()
    print(f"⚡ Processing: {command}")
    
    # Open app
    if any(cmd in command for cmd in ["open", "launch", "start"]):
        for cmd in ["open", "launch", "start"]:
            if command.startswith(cmd):
                app_name = command.replace(cmd, "").strip()
                return open_app(app_name)
    
    # System commands
    if "home" in command:
        exec_shell("input keyevent 3")
        speak_async("Going home")
        return True
    
    if "back" in command:
        exec_shell("input keyevent 4")
        speak_async("Going back")
        return True
    
    if "screenshot" in command:
        exec_shell("screencap -p /sdcard/screenshot.png")
        speak_async("Screenshot taken")
        return True
    
    speak_async(f"Done: {command}")
    return True

def main():
    speak_async("Yes boss! Dev AI ready.")
    print("\n" + "="*50)
    print("🤖 DEV AI - FIXED VERSION")
    print("Available apps:", ", ".join(APPS.keys()))
    print("Commands: open [app], home, back, screenshot")
    print("Type 'exit' to quit")
    print("="*50 + "\n")
    
    while True:
        try:
            command = input("🧑 You: ").strip()
            
            if command.lower() in ["exit", "quit", "stop"]:
                speak_async("Goodbye boss!")
                break
            
            if command:
                process_command(command)
                
        except KeyboardInterrupt:
            speak_async("Goodbye boss!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
