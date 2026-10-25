import time


class SignalFusion:
    def fuse(self, detections, attendance, audio_result):
        """Combine vision + audio into one record for this moment."""
        faces = []
        for d in detections:
            pid = d["id"]
            faces.append({
                "id": pid,
                "seconds_seen": round(attendance.seconds_seen(pid), 1),
                "present": attendance.is_present(pid),
                "movement": d.get("movement", 0.0),
            })

        if audio_result:
            audio = {
                "avg_db": audio_result["avg_db"],
                "speech_ratio": audio_result["speech_ratio"],
                "noise_ratio": audio_result["noise_ratio"],
                "silence_ratio": audio_result["silence_ratio"],
            }
        else:
            audio = {"avg_db": -80, "speech_ratio": 0,
                     "noise_ratio": 0, "silence_ratio": 1}

        return {
            "timestamp": time.time(),
            "faces": faces,
            "face_count": len(faces),
            "audio": audio,
        }