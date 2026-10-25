import csv
from datetime import datetime


class AnalyticsService:
    def summarize(self, history, attendance):
        """Reflective session summary (no ranking, no grades)."""
        if not history:
            return None

        scores = [r["score"] for r in history]
        avg = sum(scores) / len(scores)
        duration = history[-1]["timestamp"] - history[0]["timestamp"]

        # consistency: lower variation = more consistent
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)
        consistency = "steady" if variance ** 0.5 < 15 else "fluctuating"

        # split the session into 5 parts to show the timeline
        n = len(scores)
        step = max(1, n // 5)
        timeline = [round(sum(scores[i:i + step]) / len(scores[i:i + step]), 1)
                    for i in range(0, n, step)][:5]

        participants = [
            {"id": pid, "presence_seconds": round(attendance.seconds_seen(pid), 1)}
            for pid in sorted(attendance.present)
        ]

        return {
            "session_minutes": round(duration / 60, 2),
            "average_engagement": round(avg, 1),
            "peak_engagement": max(scores),
            "lowest_engagement": min(scores),
            "consistency": consistency,
            "timeline": timeline,
            "participants_present": participants,
        }

    def export_csv(self, history, filename="session_report.csv"):
        with open(filename, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["time", "score", "level", "faces", "speech_ratio"])
            for r in history:
                w.writerow([
                    datetime.fromtimestamp(r["timestamp"]).strftime("%H:%M:%S"),
                    r["score"], r["level"], r["face_count"],
                    r["audio"]["speech_ratio"],
                ])