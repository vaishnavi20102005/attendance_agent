class RecommendationsEngine:
    def generate(self, history, window=10):
        """Rule-based suggestions from recent engagement records."""
        recs = []
        if not history:
            return recs

        recent = history[-window:]
        scores = [r["score"] for r in recent]
        avg = sum(scores) / len(scores)
        latest = recent[-1]

        # Rule 1: sustained low engagement
        if avg < 40:
            recs.append({"type": "alert",
                         "message": "Engagement has been low for a while. Try an interactive activity or a quick question."})

        # Rule 2: dropping trend
        if len(scores) >= 6:
            first = sum(scores[:3]) / 3
            last = sum(scores[-3:]) / 3
            if last < first - 15:
                recs.append({"type": "warning",
                             "message": "Attention is dropping. Consider a short break or changing the pace."})

        # Rule 3: noisy classroom
        if latest["audio"]["noise_ratio"] > 0.6:
            recs.append({"type": "warning",
                         "message": "The room is noisy. A classroom management cue may help."})

        # Rule 4: nobody speaking for a long time
        if all(r["audio"]["speech_ratio"] == 0 for r in recent) and len(recent) == window:
            recs.append({"type": "info",
                         "message": "No discussion for a while. Invite questions or a short discussion."})

        # Rule 5: no one visible
        if latest["face_count"] == 0:
            recs.append({"type": "info",
                         "message": "No participants visible. Check camera position."})

        # Rule 6: high engagement
        if avg >= 70:
            recs.append({"type": "info",
                         "message": "Engagement is high. The current teaching approach is working well."})

        if not recs:
            recs.append({"type": "info",
                         "message": "Engagement is stable. Maintain the current pace."})
        return recs