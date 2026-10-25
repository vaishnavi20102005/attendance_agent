import cv2
from core.camera_service import CameraService
from core.face_detection import FaceDetector
from core.face_tracker import FaceTracker
from core.attendance_manager import AttendanceManager

camera = CameraService()
detector = FaceDetector()
tracker = FaceTracker()
attendance = AttendanceManager(threshold_seconds=5.0)
camera.start()

while True:
    frame = camera.get_frame()
    if frame is None:
        print("Could not read from webcam")
        break

    detections = detector.process_frame(frame)
    detections = tracker.update(detections)
    attendance.update(detections)

    for d in detections:
        x, y, w, h = d["bbox"]
        pid = d["id"]
        if attendance.is_present(pid):
            color, label = (0, 255, 0), f"ID {pid} PRESENT"
        else:
            color, label = (0, 165, 255), f"ID {pid} {attendance.seconds_seen(pid):.1f}s"
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.stop()
cv2.destroyAllWindows()