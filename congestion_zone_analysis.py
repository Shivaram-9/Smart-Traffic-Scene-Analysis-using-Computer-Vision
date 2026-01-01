import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

print("Press 'q' to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    zone_width = width // 3

    left_count = center_count = right_count = 0

    results = model(frame)
    annotated = results[0].plot()

    for box in results[0].boxes:
        cls = int(box.cls[0])
        label = model.names[cls]

        if label in ["car", "bus", "truck", "motorcycle"]:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx = (x1 + x2) // 2

            if cx < zone_width:
                left_count += 1
            elif cx < 2 * zone_width:
                center_count += 1
            else:
                right_count += 1

    def traffic_level(count):
        if count < 5:
            return "LOW"
        elif count < 12:
            return "MODERATE"
        else:
            return "HEAVY"

    left_status = traffic_level(left_count)
    center_status = traffic_level(center_count)
    right_status = traffic_level(right_count)

    cv2.putText(annotated, f"Left Lane: {left_status}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.putText(annotated, f"Center Lane: {center_status}",
                (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

    cv2.putText(annotated, f"Right Lane: {right_status}",
                (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    # Draw zone lines
    cv2.line(annotated, (zone_width, 0), (zone_width, height), (255,255,255), 2)
    cv2.line(annotated, (2 * zone_width, 0), (2 * zone_width, height), (255,255,255), 2)

    cv2.imshow("Traffic Congestion Zone Analysis", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
