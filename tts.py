# tts.py
import pyttsx3
import threading

class TTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        # Optional: configure voice/rate
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', int(rate * 0.95))

    def speak(self, text):
        # speak in background thread so UI is responsive
        thread = threading.Thread(target=self._speak_blocking, args=(text,), daemon=True)
        thread.start()

    def _speak_blocking(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
