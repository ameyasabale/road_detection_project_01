import cv2
from ultralytics import YOLO
import random

# Load YOLOv8 model
model = YOLO('best.pt')
names = model.names  # class index → class name

# Assign unique colors to each class
random.seed(42)
class_colors = {i: tuple(random.choices(range(50, 255), k=3)) for i in names}

# Count unique defects per class
defect_counts = {name: 0 for name in names.values()}
seen_ids = {name: set() for name in names.values()}

# Open video
cap = cv2.VideoCapture("road.mp4")
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 8 != 0:  # Skip frames to process faster
        continue

    frame = cv2.resize(frame, (1020, 600))

    # Run YOLOv8 tracking
    results = model.track(frame, persist=True)

    if results[0].boxes.id is not None:
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        class_ids = results[0].boxes.cls.int().cpu().tolist()

        for track_id, box, class_id in zip(ids, boxes, class_ids):
            x1, y1, x2, y2 = box
            label = names[class_id]

            # Count only if this track ID hasn't been seen before for this class
            if track_id not in seen_ids[label]:
                defect_counts[label] += 1
                seen_ids[label].add(track_id)

            color = class_colors[class_id]
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1 + 3, y1 - 7),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Show total unique counts on the top-left
    y_offset = 30
    for cls_name, count in defect_counts.items():
        if count > 0:
            text = f"{cls_name}: {count}"
            cv2.putText(frame, text, (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            y_offset += 25

    # Show the frame (slightly slower speed)
    cv2.imshow("FRAME", frame)
    if cv2.waitKey(10) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()

