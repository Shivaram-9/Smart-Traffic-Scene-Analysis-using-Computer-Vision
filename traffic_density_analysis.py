import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    vehicle_count = 0

    # Count vehicles
    for box in results[0].boxes:
        label = model.names[int(box.cls[0])]
        if label in ["car", "bus", "truck", "motorcycle"]:
            vehicle_count += 1

    # Traffic density logic
    if vehicle_count < 5:
        traffic_status = "LOW TRAFFIC"
        color = (0, 255, 0)
    elif vehicle_count < 15:
        traffic_status = "MODERATE TRAFFIC"
        color = (0, 255, 255)
    else:
        traffic_status = "HEAVY TRAFFIC"
        color = (0, 0, 255)

    annotated_frame = results[0].plot()

    # Display traffic status
    cv2.putText(
        annotated_frame,
        f"Traffic Status: {traffic_status}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        3
    )

    cv2.imshow("Traffic Density Analysis", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
