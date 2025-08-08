# listener.py
import os
import tempfile
import sounddevice as sd
import scipy.io.wavfile as wav
import time
import threading

from stt_vosk import VoskSTT
from tts import TTS
from verifier import VoiceVerifier
from commands import COMMAND_MAP
from gui import FloatingGUI

SAMPLE_RATE = 16000

class Assistant:
    def __init__(self, gui: FloatingGUI):
        self.stt = VoskSTT()
        self.tts = TTS()
        self.gui = gui
        self.verifier = None
        # load verifier only when enroll exists
        try:
            self.verifier = VoiceVerifier()
            print("Voice verifier loaded.")
        except Exception as e:
            print("Voice verifier unavailable:", e)
        self.wake_phrases = ["hey jarvis", "ok jarvis", "jarvis"]

    def record_temp_wav(self, duration=3, filename=None):
        if filename is None:
            fd, filename = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
        print(f"Recording test audio for {duration}s...")
        data = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
        sd.wait()
        wav.write(filename, SAMPLE_RATE, data)
        return filename

    def _is_wake(self, text):
        text = text.lower()
        for p in self.wake_phrases:
            if p in text:
                return True
        return False

    def handle_command_text(self, text):
        text = text.lower()
        print("Interpreted command:", text)
        # look for direct matches
        for phrase, func in COMMAND_MAP.items():
            if phrase in text:
                func()
                self.tts.speak(f"Executing {phrase}")
                return True
        # fallback: simple rules
        if "open google" in text or "google" in text:
            COMMAND_MAP["open google"]()
            self.tts.speak("Opening Google")
            return True
        if "youtube" in text:
            COMMAND_MAP["open youtube"]()
            self.tts.speak("Opening YouTube")
            return True
        if "portfolio" in text or "website" in text:
            COMMAND_MAP["open portfolio"]()
            self.tts.speak("Opening portfolio")
            return True
        # no match:
        self.tts.speak("Sorry, I didn't understand the command.")
        return False

    def start_listening_loop(self):
        def loop():
            while True:
                self.gui.set_status("Idle")
                print("Listening for wake word...")
                text = self.stt.listen_once(timeout=6)
                print("Heard:", text)
                if not text:
                    continue
                if self._is_wake(text):
                    self.gui.set_status("Wake word detected")
                    self.tts.speak("Yes?")
                    # record short audio for verification
                    test_path = self.record_temp_wav(duration=3)
                    if self.verifier:
                        ok, score = self.verifier.verify(test_path)
                        print("Verify:", ok, score)
                        if not ok:
                            self.gui.set_status("Not recognized")
                            self.tts.speak("Sorry, I don't recognize your voice.")
                            os.remove(test_path)
                            continue
                        else:
                            self.gui.set_status("Authenticated")
                            self.tts.speak("Welcome back.")
                    else:
                        self.gui.set_status("No verifier - skipping auth")
                    # now listen for actual command
                    self.gui.set_status("Listening...")
                    cmd_text = self.stt.listen_once(timeout=6)
                    if cmd_text:
                        self.gui.set_status("Processing")
                        self.handle_command_text(cmd_text)
                    else:
                        self.tts.speak("No command detected.")
                    # cleanup
                    try:
                        os.remove(test_path)
                    except:
                        pass
                time.sleep(0.5)

        threading.Thread(target=loop, daemon=True).start()
