import time


class FaceTracker:
    def __init__(self, max_distance=120, max_missing_seconds=4.0):
        self.max_distance = max_distance
        self.max_missing_seconds = max_missing_seconds
        self.next_id = 1
        self.tracks = {}   # id -> {"center": (x, y), "last_seen": time}

    def _center(self, bbox):
        x, y, w, h = bbox
        return (x + w / 2, y + h / 2)

    def update(self, detections):
        now = time.time()
        used_ids = set()

        for d in detections:
            c = self._center(d["bbox"])
            best_id, best_dist = None, self.max_distance

            # find the closest existing face
            for tid, t in self.tracks.items():
                if tid in used_ids:
                    continue
                dist = ((c[0] - t["center"][0]) ** 2 + (c[1] - t["center"][1]) ** 2) ** 0.5
                if dist < best_dist:
                    best_id, best_dist = tid, dist

            # no match found, so this is a new face
            if best_id is None:
                best_id = self.next_id
                self.next_id += 1

            old = self.tracks.get(best_id)
            movement = 0.0
            if old:
                movement = ((c[0] - old["center"][0]) ** 2 +
                            (c[1] - old["center"][1]) ** 2) ** 0.5
            self.tracks[best_id] = {"center": c, "last_seen": now}
            d["id"] = best_id
            d["movement"] = round(movement, 1)
            used_ids.add(best_id)

        # forget faces not seen for a while
        self.tracks = {
            tid: t for tid, t in self.tracks.items()
            if now - t["last_seen"] <= self.max_missing_seconds
        }
        return detections