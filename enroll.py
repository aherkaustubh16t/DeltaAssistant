# enroll.py
import sounddevice as sd
import scipy.io.wavfile as wav
import os

def record(duration=6, samplerate=16000, filename="data/enroll.wav"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    print(f"Recording {duration} seconds. Speak naturally...")
    recording = sd.rec(int(duration*samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, samplerate, recording)
    print(f"Saved enrollment to {filename}")

if __name__ == "__main__":
    record()
