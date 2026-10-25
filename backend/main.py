import sys
import cv2
from core.camera_service import CameraService
from core.face_detection import FaceDetector
from core.face_tracker import FaceTracker
from core.attendance_manager import AttendanceManager
from core.audio_worker import AudioWorker
from core.multimodal_agent import MultimodalAgent
from core.recommendations_engine import RecommendationsEngine
from core.analytics_service import AnalyticsService

# Usage:
#   python main.py              -> live webcam
#   python main.py video.mp4    -> pre-recorded video (no live audio)
source = sys.argv[1] if len(sys.argv) > 1 else None

camera = CameraService()
detector = FaceDetector()
tracker = FaceTracker()
attendance = AttendanceManager(threshold_seconds=5.0)
agent = MultimodalAgent()
engine = RecommendationsEngine()
analytics = AnalyticsService()

audio_worker = None
if source is None:
    camera.start()
    audio_worker = AudioWorker()
    audio_worker.start()
else:
    camera.cap = cv2.VideoCapture(source)
    camera.is_running = True

frame_no = 0
suggestions = []

while True:
    frame = camera.get_frame()
    if frame is None:
        print("End of video or camera not available")
        break

    detections = tracker.update(detector.process_frame(frame))
    attendance.update(detections)
    latest_audio = audio_worker.latest if audio_worker else None
    record = agent.process(detections, attendance, latest_audio)

    frame_no += 1
    if frame_no % 30 == 0:
        suggestions = engine.generate(agent.history)

    for d in detections:
        x, y, w, h = d["bbox"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {d['id']}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Engagement: {record['score']} ({record['level']})",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    if suggestions:
        cv2.putText(frame, suggestions[0]["message"][:60], (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    cv2.imshow("Multimodal Attendance & Engagement Agent", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

if audio_worker:
    audio_worker.stop()
camera.stop()
cv2.destroyAllWindows()

if agent.history:
    print("\n--- Suggestions ---")
    for rec in engine.generate(agent.history):
        print(f"[{rec['type']}] {rec['message']}")
    summary = analytics.summarize(agent.history, attendance)
    print("\n--- Session summary ---")
    for k, v in summary.items():
        print(f"{k}: {v}")
    analytics.export_csv(agent.history)
    print("\nSaved session_report.csv")