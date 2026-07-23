import os
import sys
import time
import json
import base64
import subprocess
import threading
import queue
from datetime import datetime

# ===== CONFIGURATION =====
API_KEY = os.getenv("GEMINI_API_KEY", "")
WAKE_WORDS = ["dev", "hey dev", "hello dev", "hi dev"]
LANGUAGES = {"en": "en-US", "hi": "hi-IN", "ne": "ne-NP"}

# ===== VOICE FUNCTIONS =====
def speak(text, lang="en"):
    """Voice output with language support."""
    print(f"🤖 Dev: {text}")
    lang_code = LANGUAGES.get(lang, "en-US")
    os.system(f'termux-tts-speak "{text}" -l {lang_code} 2>/dev/null')

def listen_voice(timeout=5):
    """Listen for voice with timeout."""
    try:
        output = subprocess.check_output(
            ["termux-speech-to-text"], 
            timeout=timeout
        ).decode("utf-8").strip()
        if output:
            return output.lower()
    except subprocess.TimeoutExpired:
        return None
    except:
        return None
    return None

# ===== SCREEN VISION ENGINE =====
class VisionEngine:
    def capture(self, path="screen.jpg"):
        """Take screenshot."""
        os.system(f'rish -c "screencap -p /sdcard/{path}" 2>/dev/null')
        os.system(f'mv /sdcard/{path} ./ 2>/dev/null')
        return path

    def analyze_screen(self, command):
        """Use Gemini Vision to understand screen and decide action."""
        screen = self.capture()
        
        prompt = f"""
        You are Dev AI - a mobile assistant controlling this Android screen.
        User command: "{command}"
        
        Analyze the screen image and determine what action to take.
        Return ONLY valid JSON:
        {{
            "action": "tap|swipe|type|open_app|scroll|home|back|screenshot|build|deploy|speak",
            "x": 0, "y": 0, "x2": 0, "y2": 0,
            "text": "",
            "app": "",
            "confidence": 0.0
        }}
        """
        
        # Call Gemini Vision API
        response = self.call_gemini_vision(prompt, screen)
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        return {"action": "speak", "text": "Could not understand"}

    def call_gemini_vision(self, prompt, image_path):
        """Call Gemini API with image."""
        if not API_KEY:
            return '{"action": "speak", "text": "No API key"}'
        
        # Read and encode image
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                ]
            }]
        }
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        try:
            req = urllib.request.Request(
                url, 
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                return result['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f'{{"action": "speak", "text": "Error: {str(e)}"}}'

# ===== ACTION ENGINE =====
class ActionEngine:
    def __init__(self):
        self.vision = VisionEngine()
    
    def execute(self, action_data):
        """Execute the action determined by AI."""
        action = action_data.get("action", "speak")
        
        if action == "tap":
            x = action_data.get("x", 540)
            y = action_data.get("y", 960)
            os.system(f'rish -c "input tap {x} {y}" 2>/dev/null')
            return f"Tapped at ({x}, {y})"
        
        elif action == "swipe":
            x1 = action_data.get("x", 540)
            y1 = action_data.get("y", 1500)
            x2 = action_data.get("x2", 540)
            y2 = action_data.get("y2", 500)
            duration = action_data.get("duration", 300)
            os.system(f'rish -c "input swipe {x1} {y1} {x2} {y2} {duration}" 2>/dev/null')
            return f"Swiped from ({x1},{y1}) to ({x2},{y2})"
        
        elif action == "type":
            text = action_data.get("text", "")
            formatted = text.replace(" ", "%s")
            os.system(f'rish -c "input text {formatted}" 2>/dev/null')
            return f"Typed: {text}"
        
        elif action == "open_app":
            app = action_data.get("app", "")
            os.system(f'rish -c "monkey -p {app} 1" 2>/dev/null')
            return f"Opening: {app}"
        
        elif action == "home":
            os.system('rish -c "input keyevent 3" 2>/dev/null')
            return "Going home"
        
        elif action == "back":
            os.system('rish -c "input keyevent 4" 2>/dev/null')
            return "Going back"
        
        elif action == "screenshot":
            os.system('rish -c "screencap -p /sdcard/screenshot.png" 2>/dev/null')
            return "Screenshot taken"
        
        elif action == "scroll":
            direction = action_data.get("direction", "down")
            if direction == "up":
                os.system('rish -c "input swipe 540 400 540 1200 200" 2>/dev/null')
            else:
                os.system('rish -c "input swipe 540 1200 540 400 200" 2>/dev/null')
            return f"Scrolling {direction}"
        
        elif action == "build":
            return self.build_project(action_data)
        
        elif action == "deploy":
            return self.deploy_project(action_data)
        
        else:
            return action_data.get("text", "Action completed")

    def build_project(self, data):
        """Build websites, apps, games via voice."""
        project_type = data.get("type", "website")
        description = data.get("description", "")
        
        if project_type == "website":
            return self.build_website(description)
        elif project_type == "app":
            return self.build_app(description)
        elif project_type == "game":
            return self.build_game(description)
        return "Project type not supported"

    def build_website(self, description):
        """Generate a complete website."""
        if not API_KEY:
            return "No API key for generation"
        
        prompt = f"Create complete HTML/CSS/JS for: {description}. Include modern design."
        response = self.call_gemini(prompt)
        
        if response:
            with open("index.html", "w") as f:
                f.write(response)
            return "Website created: index.html"
        return "Failed to generate website"

    def build_app(self, description):
        """Generate a mobile app."""
        prompt = f"Create complete Python/Flask app for: {description}"
        response = self.call_gemini(prompt)
        if response:
            with open("app.py", "w") as f:
                f.write(response)
            return "App created: app.py"
        return "Failed to generate app"

    def build_game(self, description):
        """Generate a game."""
        prompt = f"Create complete HTML game for: {description}"
        response = self.call_gemini(prompt)
        if response:
            with open("game.html", "w") as f:
                f.write(response)
            return "Game created: game.html"
        return "Failed to generate game"

    def deploy_project(self, data):
        """Deploy to platforms."""
        platform = data.get("platform", "github")
        if platform == "github":
            os.system('git init && git add . && git commit -m "AI deployed"')
            return "Ready for GitHub push"
        elif platform == "netlify":
            os.system('netlify deploy --prod')
            return "Deployed to Netlify"
        elif platform == "vercel":
            os.system('vercel --prod')
            return "Deployed to Vercel"
        return "Deployment platform not found"

    def call_gemini(self, prompt):
        """Call Gemini API for text."""
        if not API_KEY:
            return None
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                return result['candidates'][0]['content']['parts'][0]['text']
        except:
            return None

# ===== MAIN ASSISTANT =====
class DevAssistant:
    def __init__(self):
        self.engine = ActionEngine()
        self.vision = VisionEngine()
        self.running = True
        self.lang = "en"

    def start(self):
        speak("Yes boss! Dev AI is fully ready.", self.lang)
        print("\n" + "="*60)
        print("🚀 DEV ULTIMATE AI ASSISTANT")
        print("Features: Vision control | Voice commands | Build projects")
        print("Languages: English | Hindi | Nepali")
        print("Say: 'Hey Dev' to wake me up")
        print("Type: 'exit' to quit")
        print("="*60 + "\n")

        while self.running:
            # Listen for wake word
            print("🎙️ Waiting for wake word...")
            heard = listen_voice(3)
            
            if heard:
                if any(w in heard for w in WAKE_WORDS):
                    speak("Yes boss! What can I do?", self.lang)
                    
                    # Listen for command
                    command = listen_voice(5)
                    if command:
                        print(f"📝 Command: {command}")
                        self.process_command(command)
            
            time.sleep(0.5)

    def process_command(self, command):
        """Process user command with vision AI."""
        # Check if command contains build/deploy keywords
        if any(kw in command for kw in ["build", "create", "make", "generate"]):
            if "website" in command:
                description = command.replace("build", "").replace("website", "").strip()
                result = self.engine.build_website(description)
                speak(f"Boss! {result}", self.lang)
                return
            
            if "app" in command:
                description = command.replace("build", "").replace("app", "").strip()
                result = self.engine.build_app(description)
                speak(f"Boss! {result}", self.lang)
                return
            
            if "game" in command:
                description = command.replace("build", "").replace("game", "").strip()
                result = self.engine.build_game(description)
                speak(f"Boss! {result}", self.lang)
                return

        # Check for app open commands
        if "open" in command:
            app_map = {
                "flipaclip": "com.vblast.flipaclip",
                "alight": "com.alightcreative.motion",
                "prisma": "com.prisma3D.prisma3D",
                "youtube": "com.google.android.youtube",
                "whatsapp": "com.whatsapp",
                "instagram": "com.instagram.android",
                "chrome": "com.android.chrome",
                "settings": "com.android.settings"
            }
            
            for name, package in app_map.items():
                if name in command:
                    self.engine.execute({"action": "open_app", "app": package})
                    speak(f"Opening {name}", self.lang)
                    return

        # Use vision for everything else
        speak("Analyzing screen boss...", self.lang)
        action = self.vision.analyze_screen(command)
        result = self.engine.execute(action)
        speak(f"Boss! {result}", self.lang)

# ===== RUN =====
if __name__ == "__main__":
    # Import urllib for API calls
    import urllib.request
    
    # Check API key
    if not API_KEY:
        print("⚠️  Set your GEMINI_API_KEY first!")
        print("export GEMINI_API_KEY='your_key_here'")
        sys.exit(1)
    
    assistant = DevAssistant()
    assistant.start()
