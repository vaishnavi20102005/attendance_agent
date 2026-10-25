import numpy as np
import sounddevice as sd


class AudioService:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def record(self, seconds=2.0):
        """Record from the microphone and return a 1D numpy array."""
        audio = sd.rec(
            int(seconds * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        return audio.flatten()