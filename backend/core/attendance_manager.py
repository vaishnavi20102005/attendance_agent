import csv
import os
import time
from datetime import datetime


class AttendanceManager:
    def __init__(self, threshold_seconds=5.0, log_file="attendance_log.csv"):
        self.threshold = threshold_seconds
        self.log_file = log_file
        self.presence = {}    # id -> total seconds seen
        self.last_time = {}   # id -> last time we updated this id
        self.present = set()  # ids already marked present

        # create the CSV with a header if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", newline="") as f:
                csv.writer(f).writerow(["participant_id", "presence_seconds", "marked_at"])

    def update(self, detections):
        now = time.time()
        for d in detections:
            pid = d["id"]
            if pid in self.last_time:
                gap = now - self.last_time[pid]
                if gap < 1.0:   # only count continuous time, ignore long gaps
                    self.presence[pid] = self.presence.get(pid, 0) + gap
            else:
                self.presence[pid] = 0
            self.last_time[pid] = now

            if self.presence[pid] >= self.threshold and pid not in self.present:
                self.present.add(pid)
                self._save(pid)

    def _save(self, pid):
        with open(self.log_file, "a", newline="") as f:
            csv.writer(f).writerow([
                pid,
                round(self.presence[pid], 1),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ])
        print(f"Participant {pid} marked PRESENT")

    def is_present(self, pid):
        return pid in self.present

    def seconds_seen(self, pid):
        return self.presence.get(pid, 0)