import cv2
from ultralytics import YOLO
import src.speech as speech

model = YOLO("yolo11n.pt")
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    raise RuntimeError("Camera could not be opened")
# Track whether a visitor has already been greeted
greeted = False
while True:
    ret,frame = camera.read()
    if not ret:
        print("Failed to read camera frame")
        break

    results = model(frame,verbose=False)
    visitor_detected = False
    for result in results:
        for box in result.boxes:
            class_id = int (box.cls[0])
            confidence = float(box.conf[0])

            if class_id==0 and confidence > 0.6:
                visitor_detected = True
    if visitor_detected and not greeted:
        speech.greet()
        greeted = True

    elif not visitor_detected:
        greeted = False

    cv2.imshow("Robot Recepcionist Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()



