from ultralytics import YOLO
import cv2
import time
#loads the pretrained YOLO11 nano model for person detection.
model = YOLO("yolo11n.pt")
#analyses a single camera frame and checks whether a person is present.
#returns true when person is detected with confidence greater than %60.
def detect_visitor(frame):
    results = model(frame, verbose=False)
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            if class_id == 0 and confidence > 0.6:
                return True
    return False
#continously monitors the camera for visitors.
# calls the supplied on_visitor function when a new visitor is detected.
# a session timeout prevents the same visitor from being greeted repeatedly.
def watch_for_visitors(on_visitor):
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError("Camera could not be opened")

    greeted = False
    last_seen_time = None
    session_timeout = 5

    try:
        while True:
            ret, frame = camera.read()

            if not ret:
                print("Failed to read camera frame")
                break

            visitor_detected = detect_visitor(frame)

            if visitor_detected:
                last_seen_time = time.monotonic()

                if not greeted:
                    greeted = True
                    on_visitor()

            elif greeted and last_seen_time is not None:
                if time.monotonic() - last_seen_time >= session_timeout:
                    greeted = False
                    print("Visitor session ended")

            cv2.imshow("Robot Receptionist Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()
