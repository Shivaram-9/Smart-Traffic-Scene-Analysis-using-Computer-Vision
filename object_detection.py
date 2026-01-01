import cv2
from ultralytics import YOLO
import os

# Create outputs folder if not exists
os.makedirs("outputs", exist_ok=True)

# Load YOLO model (auto-downloads if not present)
model = YOLO("yolov8n.pt")

# Read image
image = cv2.imread("dataset/images/test.jpg")

# Run object detection
results = model(image)

# Draw detections
for r in results:
    for box in r.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls = int(box.cls[0])
        conf = box.conf[0]

        label = f"{model.names[cls]} {conf:.2f}"

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            image,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

# # Save output instead of showing window
# output_path = "outputs/object_detection.png"
# cv2.imwrite(output_path, image)

# print(f"Object detection completed.")
# print(f"Result saved at: {output_path}")

# Save output
output_path = "outputs/object_detection.png"
cv2.imwrite(output_path, image)

# Show output image
cv2.imshow("Object Detection Output", image)
cv2.waitKey(3000)   # shows for 3 seconds
cv2.destroyAllWindows()

print(f"Object detection completed.")
print(f"Result saved at: {output_path}")

