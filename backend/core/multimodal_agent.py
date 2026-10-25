from core.fusion import SignalFusion
from core.engagement_scorer import EngagementScorer


class MultimodalAgent:
    def __init__(self):
        self.fusion = SignalFusion()
        self.scorer = EngagementScorer()
        self.history = []   # engagement over time

    def process(self, detections, attendance, audio_result):
        fused = self.fusion.fuse(detections, attendance, audio_result)
        result = self.scorer.score(fused)
        record = {**fused, **result}
        self.history.append(record)
        return record