import cv2


class FaceDetector:
    def __init__(self):
        path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(path)
        if self.face_cascade.empty():
            print("Error: could not load face cascade xml")

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)

        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=7, minSize=(90, 90)
        )

        # keep only the largest face (closest person to the camera)
        if len(faces) > 1:
            faces = [max(faces, key=lambda f: f[2] * f[3])]

        detections = []
        for (x, y, w, h) in faces:
            detections.append({"bbox": (int(x), int(y), int(w), int(h))})
        return detections