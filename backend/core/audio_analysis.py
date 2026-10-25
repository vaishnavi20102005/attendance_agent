import numpy as np
import librosa


class AudioAnalyzer:
    def __init__(self, sample_rate=16000, frame_seconds=0.5):
        self.sample_rate = sample_rate
        self.frame_size = int(sample_rate * frame_seconds)

    def prepare(self, audio_data):
        """Convert raw audio into a clean float array."""
        if isinstance(audio_data, bytes):
            y = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        else:
            y = np.asarray(audio_data, dtype=np.float32)
        if y.ndim > 1:
            y = y.mean(axis=1)
        return y

    def split_into_windows(self, y):
        """Cut the signal into fixed 0.5 second windows."""
        windows = []
        for i in range(0, len(y) - self.frame_size + 1, self.frame_size):
            windows.append(y[i:i + self.frame_size])
        return windows

    def analyze_window(self, window):
        """Measure one window and give it a label."""
        rms = float(np.sqrt(np.mean(window ** 2)))     # loudness (energy)
        db = float(20 * np.log10(rms + 1e-10))         # loudness in decibels
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(window)))

        if rms < 0.010:
            label = "silence"
        elif rms < 0.025:
            label = "noise"
        else:
            label = "speech"
        return {"rms": round(rms, 4), "db": round(db, 1),
                "zcr": round(zcr, 3), "label": label}

    def analyze_chunk(self, audio_data):
        """Analyze a whole recording and return summary numbers."""
        y = self.prepare(audio_data)
        windows = self.split_into_windows(y)[1:]
        if not windows:
            return None

        results = [self.analyze_window(w) for w in windows]
        labels = [r["label"] for r in results]
        total = len(labels)

        return {
            "avg_db": round(float(np.mean([r["db"] for r in results])), 1),
            "speech_ratio": round(labels.count("speech") / total, 2),
            "noise_ratio": round(labels.count("noise") / total, 2),
            "silence_ratio": round(labels.count("silence") / total, 2),
            "windows": results,
        }