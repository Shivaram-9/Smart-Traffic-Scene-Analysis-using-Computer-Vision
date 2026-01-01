import cv2
import csv
from datetime import datetime
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

# Create CSV file if not exists
csv_file = "outputs/traffic_log.csv"

with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(["Time", "Cars", "Motorcycles", "Buses", "Trucks", "Traffic_Status"])

print("Press 'q' to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    car = motorcycle = bus = truck = 0

    for box in results[0].boxes:
        label = model.names[int(box.cls[0])]
        if label == "car":
            car += 1
        elif label == "motorcycle":
            motorcycle += 1
        elif label == "bus":
            bus += 1
        elif label == "truck":
            truck += 1

    total_vehicles = car + motorcycle + bus + truck

    if total_vehicles < 5:
        traffic_status = "LOW"
        color = (0, 255, 0)
    elif total_vehicles < 15:
        traffic_status = "MODERATE"
        color = (0, 255, 255)
    else:
        traffic_status = "HEAVY"
        color = (0, 0, 255)

    annotated = results[0].plot()

    cv2.putText(
        annotated,
        f"Cars:{car} Bikes:{motorcycle} Bus:{bus} Truck:{truck}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated,
        f"Traffic: {traffic_status}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        3
    )

    # Log data every frame
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%H:%M:%S"),
            car, motorcycle, bus, truck, traffic_status
        ])

    cv2.imshow("Traffic Data Logging", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
