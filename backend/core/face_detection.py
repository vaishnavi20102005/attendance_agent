import cv2


class FaceDetector:
    def __init__(self):
        path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(path)
        if self.face_cascade.empty():
            print("Error: could not load face cascade xml")

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=7, minSize=(80, 80)
        )
        detections = []
        for (x, y, w, h) in faces:
            detections.append({"bbox": (int(x), int(y), int(w), int(h))})
        return detections

    