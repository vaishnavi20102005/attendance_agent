from core.audio_service import AudioService
from core.audio_analysis import AudioAnalyzer

audio = AudioService()
analyzer = AudioAnalyzer()

print("Recording 5 seconds... stay silent, then talk, then stay quiet again")
signal = audio.record(5.0)

result = analyzer.analyze_chunk(signal)
print("Average noise (dB):", result["avg_db"])
print("Speech ratio:", result["speech_ratio"])
print("Noise ratio:", result["noise_ratio"])
print("Silence ratio:", result["silence_ratio"])
print()
for i, w in enumerate(result["windows"]):
    print(f"Window {i}: {w['label']:8} rms={w['rms']}")