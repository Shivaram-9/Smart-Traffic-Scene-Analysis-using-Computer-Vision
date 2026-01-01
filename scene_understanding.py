from ultralytics import YOLO
import cv2
import os
import numpy as np

os.makedirs("outputs", exist_ok=True)

model = YOLO("yolov8n.pt")
image = cv2.imread("dataset/images/test.jpg")
results = model(image)

object_count = {}
for r in results:
    for box in r.boxes:
        label = model.names[int(box.cls[0])]
        object_count[label] = object_count.get(label, 0) + 1

if object_count.get("car", 0) > 5:
    scene = "Urban Traffic Road"
    conclusion = "Heavy traffic detected"
else:
    scene = "Normal Scene"
    conclusion = "Normal activity"

text_lines = [
    "Scene Understanding Result",
    "",
    *[f"{k}: {v}" for k, v in object_count.items()],
    "",
    f"Scene Type: {scene}",
    f"Conclusion: {conclusion}"
]

canvas = np.ones((400, 700, 3), dtype=np.uint8) * 255
y = 40
for line in text_lines:
    cv2.putText(canvas, line, (20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    y += 35

# cv2.imwrite("outputs/scene_understanding.png", canvas)
# print("Scene understanding result saved to outputs/scene_understanding.png")

img = cv2.imread("outputs/scene_understanding.png")
cv2.imshow("Scene Understanding Output", img)
cv2.waitKey(3000)
cv2.destroyAllWindows()
