import os
import time
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

# Target Wake Words
WAKE_WORDS = ["dev", "hey dev", "hello dev", "hi dev"]

class DevAIWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(DevAIWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        # UI Header
        self.title_label = Label(
            text="[b]DEV AI AGENT[/b]\nStandalone App Mode",
            markup=True,
            font_size='24sp',
            halign='center'
        )
        self.add_widget(self.title_label)

        # Status Display
        self.status_label = Label(
            text="Status: 🔴 Listening for 'Hey Dev'...",
            font_size='18sp',
            halign='center'
        )
        self.add_widget(self.status_label)

        # Quick Control Button
        self.action_btn = Button(
            text="Voice Assistant Active",
            size_hint=(1, 0.3),
            background_color=(0, 0.8, 1, 1)
        )
        self.add_widget(self.action_btn)

        # Start Background Wake Word Service Thread
        threading.Thread(target=self.wake_word_loop, daemon=True).start()

    def update_status(self, text):
        def _update(dt):
            self.status_label.text = text
        Clock.schedule_once(_update)

    def speak_response(self, text):
        """Native voice response."""
        print(f"🤖 Dev Voice Output: {text}")
        os.system(f'termux-tts-speak "{text}" 2>/dev/null || true')

    def wake_word_loop(self):
        """Background continuous wake word detection loop."""
        while True:
            # Passive local microphone check placeholder
            time.sleep(2)
            # When speech triggers:
            # self.speak_response("Yes boss")

class DevAIApp(App):
    def build(self):
        return DevAIWidget()

if __name__ == "__main__":
    DevAIApp().run()
