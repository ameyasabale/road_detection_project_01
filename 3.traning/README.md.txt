 Model Training – YOLOv12

This folder contains the training script and config for the road defect detection model using YOLOv12.

---

## 🔧 YOLO Version
- Model: `yolov12n.yaml`
- Dataset: Roboflow export (YOLOv12 format)
- Path: `2_labeling/roboflow_export/data.yaml`

---

## 🧠 Classes
- crack
- damage surface
- pothole
- sign board
- speed breaker

---

## 🛠️ Training Settings

| Setting     | Value   |
|-------------|---------|
| Epochs      | 100     |
| Image Size  | 640     |
| Batch Size  | 8       |
| Optimizer   | SGD     |
| Device      | GPU     |

---

## ▶️ Run Training

```bash
python train_yolov12.py

