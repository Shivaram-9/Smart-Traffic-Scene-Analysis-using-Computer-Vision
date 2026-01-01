import cv2
from ultralytics import YOLO
from collections import defaultdict

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

track_history = defaultdict(list)

print("Press 'q' to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(frame, persist=True)

    annotated = results[0].plot()

    if results[0].boxes.id is not None:
        ids = results[0].boxes.id.int().tolist()
        boxes = results[0].boxes.xyxy.tolist()

        for box, track_id in zip(boxes, ids):
            x1, y1, x2, y2 = map(int, box)
            cv2.putText(
                annotated,
                f"ID {track_id}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2
            )

    cv2.imshow("Vehicle Tracking", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
