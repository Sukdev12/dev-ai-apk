def listen_voice():
    """Listen for voice command using Termux native speech-to-text."""
    print("\n🎙️ Listening...")
    try:
        # Use termux-speech-to-text (no PyAudio needed)
        output = subprocess.check_output(["termux-speech-to-text"]).decode("utf-8").strip()
        if output:
            print(f"🗣️ You said: {output}")
            return output.lower()
    except Exception as e:
        print(f"⚠️ Voice error: {e}")
        return None
