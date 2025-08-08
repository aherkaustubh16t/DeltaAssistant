# stt_vosk.py
import os
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel
import json

SetLogLevel(0)

VOSK_MODEL_PATH = "data/vosk-model"  # set to the extracted model folder

class VoskSTT:
    def __init__(self, device=None, samplerate=16000, model_path=VOSK_MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Vosk model folder not found at {model_path}. Download and extract a model.")
        self.model = Model(model_path)
        self.samplerate = samplerate
        self.device = device
        self.q = queue.Queue()
        self.rec = None

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(bytes(indata))

    def start_stream(self):
        self.q.queue.clear()
        self.stream = sd.InputStream(samplerate=self.samplerate, device=self.device, channels=1, dtype='int16', callback=self.audio_callback)
        self.stream.start()
        self.rec = KaldiRecognizer(self.model, self.samplerate)

    def stop_stream(self):
        if hasattr(self, "stream"):
            self.stream.stop()
            self.stream.close()

    def listen_once(self, timeout=5):
        """Records up to `timeout` seconds and returns recognized text (best-effort)."""
        self.start_stream()
        import time
        start = time.time()
        result_text = ""
        while time.time() - start < timeout:
            try:
                data = self.q.get(timeout=timeout)
            except queue.Empty:
                break
            if self.rec.AcceptWaveform(data):
                res = json.loads(self.rec.Result())
                result_text += " " + res.get("text", "")
            else:
                # partial = json.loads(self.rec.PartialResult())
                pass
        # final
        res = json.loads(self.rec.FinalResult())
        result_text += " " + res.get("text", "")
        self.stop_stream()
        return result_text.strip()

    def listen(self, timeout=5):
        """Records up to `timeout` seconds and returns recognized text (best-effort)."""
        self.start_stream()
        import time
        start = time.time()
        result_text = ""
        while time.time() - start < timeout:
            try:
                data = self.q.get(timeout=timeout)
            except queue.Empty:
                break
            if self.rec.AcceptWaveform(data):
                res = json.loads(self.rec.Result())
                result_text += " " + res.get("text", "")
            else:
                # partial = json.loads(self.rec.PartialResult())
                pass
        self.stop_stream()
        return result_text