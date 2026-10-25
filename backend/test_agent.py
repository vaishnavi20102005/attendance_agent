import cv2
from core.camera_service import CameraService
from core.face_detection import FaceDetector
from core.face_tracker import FaceTracker
from core.attendance_manager import AttendanceManager
from core.audio_worker import AudioWorker
from core.multimodal_agent import MultimodalAgent

camera = CameraService()
detector = FaceDetector()
tracker = FaceTracker()
attendance = AttendanceManager(threshold_seconds=5.0)
audio_worker = AudioWorker()
agent = MultimodalAgent()

camera.start()
audio_worker.start()

while True:
    frame = camera.get_frame()
    if frame is None:
        print("Could not read from webcam")
        break

    detections = tracker.update(detector.process_frame(frame))
    attendance.update(detections)

    record = agent.process(detections, attendance, audio_worker.latest)

    for d in detections:
        x, y, w, h = d["bbox"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {d['id']}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Engagement: {record['score']} ({record['level']})",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imshow("Agent", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

audio_worker.stop()
camera.stop()
cv2.destroyAllWindows()

if agent.history:
    scores = [r["score"] for r in agent.history]
    print("Last result:", agent.history[-1]["score"], agent.history[-1]["level"])
    for r in agent.history[-1]["reasons"]:
        print(" -", r)
    print("Frames analyzed:", len(scores))
    print("Average score:", round(sum(scores) / len(scores), 1))
    print("Highest score:", max(scores))