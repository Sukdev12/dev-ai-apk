import os
import sys
import time
import subprocess

WAKE_WORDS = ["dev", "hey dev", "hello dev", "hi dev"]

def speak(text):
    """Voice output using native Android TTS."""
    print(f"🤖 Dev: {text}")
    os.system(f'termux-tts-speak "{text}"')

def listen_for_audio():
    """Captures quick audio via Termux Speech API."""
    try:
        output = subprocess.check_output(["termux-speech-to-text"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
        return output.lower() if output else ""
    except Exception:
        return ""

def process_command(user_cmd):
    """Processes task after wake word is activated."""
    print(f"⚡ Processing task: {user_cmd}")
    
    # Quick launcher logic
    if "open" in user_cmd or "kholo" in user_cmd:
        if "youtube" in user_cmd:
            os.system("rish -c 'am start -n com.google.android.youtube/com.google.android.apps.youtube.app.watchwhile.WatchWhileActivity' 2>/dev/null || adb shell monkey -p com.google.android.youtube 1")
        elif "chrome" in user_cmd:
            os.system("rish -c 'am start -n com.android.chrome/com.google.android.apps.chrome.Main' 2>/dev/null || adb shell monkey -p com.android.chrome 1")
    
    # Task completion feedback
    speak("Task completed, boss!")

def main():
    print("==================================================")
    print("🎙️ DEV AI WAKE WORD ENGINE IS ACTIVE")
    print("Say: 'Hey Dev', 'Hello Dev', or 'Hi Dev'")
    print("==================================================")
    
    while True:
        # Passive listening loop for wake words
        heard = listen_for_audio()
        
        if heard:
            print(f"👂 Heard: '{heard}'")
            
            # Check if any wake word was spoken
            if any(wake_word in heard for wake_word in WAKE_WORDS):
                # 1. Immediate Voice Acknowledgment
                speak("Yes boss")
                time.sleep(0.5)
                
                # 2. Extract command if spoken in the same sentence
                command_text = heard
                for wake_word in WAKE_WORDS:
                    command_text = command_text.replace(wake_word, "").strip()
                
                # 3. If command wasn't in the same breath, listen for the follow-up task
                if not command_text:
                    print("🎙️ Listening for task...")
                    command_text = listen_for_audio()
                
                if command_text:
                    process_command(command_text)

if __name__ == "__main__":
    main()
