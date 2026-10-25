class EngagementScorer:
    def score(self, fused):
        """Rule-based score from 0 to 100, with the reasons."""
        score = 0
        reasons = []

        # Rule 1: visual presence (up to 40 points)
        if fused["face_count"] == 0:
            reasons.append("No faces visible")
        else:
            present = [f for f in fused["faces"] if f["present"]]
            if present:
                score += 40
                reasons.append("Participants sustained presence (+40)")
            else:
                score += 20
                reasons.append("Faces visible but not yet confirmed (+20)")

            # Rule 2: movement (up to 20 points)
            avg_move = sum(f["movement"] for f in fused["faces"]) / len(fused["faces"])
            if 1 <= avg_move <= 40:
                score += 20
                reasons.append("Natural movement detected (+20)")
            elif avg_move < 1:
                score += 5
                reasons.append("Very little movement, possible inactivity (+5)")
            else:
                score += 10
                reasons.append("Excessive movement (+10)")

        # Rule 3: audio activity (up to 40 points)
        audio = fused["audio"]
        if audio["speech_ratio"] >= 0.3:
            score += 40
            reasons.append("Active speech in the room (+40)")
        elif audio["speech_ratio"] > 0 or audio["noise_ratio"] > 0.3:
            score += 20
            reasons.append("Some sound activity (+20)")
        else:
            reasons.append("Room is silent (+0)")

        if score >= 70:
            level = "High"
        elif score >= 40:
            level = "Medium"
        else:
            level = "Low"

        return {"score": score, "level": level, "reasons": reasons}