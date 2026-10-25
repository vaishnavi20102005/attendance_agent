import threading
from core.audio_service import AudioService
from core.audio_analysis import AudioAnalyzer


class AudioWorker:
    def __init__(self, chunk_seconds=1.5):
        self.audio = AudioService()
        self.analyzer = AudioAnalyzer()
        self.chunk_seconds = chunk_seconds
        self.latest = None      # newest audio result
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def _loop(self):
        while self.running:
            try:
                signal = self.audio.record(self.chunk_seconds)
                self.latest = self.analyzer.analyze_chunk(signal)
            except Exception as e:
                # no microphone or access blocked: continue without audio
                print("Audio unavailable:", e)
                self.latest = None
                break

    def stop(self):
        self.running = False