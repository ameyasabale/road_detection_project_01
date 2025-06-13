# Road Defect Detection Using YOLOv12 and GPS Mapping 🛣️📍

This project detects road defects like potholes, cracks, and damaged surfaces using YOLOv12 and plots their real-world locations using GPS and interactive maps. It also includes full visualization, reporting, and automation steps in a modular pipeline.

---

## 🔁 Pipeline Overview

| Step | Folder                | Description |
|------|------------------------|-------------|
| 1️⃣   | `1_data_preparation/` | Extract image frames from input road video |
| 2️⃣   | `2_labeling/`         | Annotate frames in Roboflow and export YOLOv12 dataset |
| 3️⃣   | `3_training/`         | Train YOLOv12 model on labeled data to generate `best.pt` |
| 4️⃣   | `4_gps_ocr/`          | Extract GPS coordinates from images and reverse geocode to location |
| 5️⃣   | `5_detection/`        | Detect defects on frames, overlay bounding boxes and location |
| 6️⃣   | `6_visualization/`    | Plot all defects on an interactive map using Folium |
| 7️⃣   | `7_reports/`          | Summarize results, generate defect counts and final reports |

---

## 🧠 Technologies Used

- 📦 Python, OpenCV, Pandas, Pillow
- 🧠 YOLOv12 via Ultralytics
- 🌐 Roboflow (for labeling)
- 📍 Folium + OpenStreetMap APIs
- 🧾 Jupyter Notebook / Thonny

---


---

## 🗂️ Input Files

- `road.mp4` – Original video
- `best.pt` – Trained YOLO model
- `final_output1.csv` – Master detection + location data
- `data.yaml` – Class mapping for YOLO training

---

## 📤 Output Files

- Labeled frames with bounding boxes and location overlays
- `map.html` with geolocated defect markers
- `defect_summary.csv` with class-wise counts
- Optional: PDF report + sample images

---

## ▶️ Run Order

```bash

# Step-by-step flow
1️⃣ python frame_extraction.py
2️⃣ Annotate using Roboflow, export YOLOv12 format
3️⃣ Train YOLO → save best.pt
4️⃣ Extract GPS → final_output1.csv
5️⃣ python visualize_frames_with_location.py
6️⃣ python map_defect_locations.py
7️⃣ Generate CSV summaries or PDF report

📌 Results Snapshot
Defect Type	Count
Pothole	643
Damage Surface	257
Cracks	19
Sign Board	11
Speed Breaker	8

✅ Project Highlights
🔍 Detects multiple road defects with high accuracy

🛰️ Extracts GPS from image overlays using OCR

🌍 Maps defect locations on an interactive dashboard

📸 Visual output for every frame with location

📊 Final report ready for submission

💡 Author

👨‍💻 Name: Ameya Sabale

🔗 GitHub: ameyasabale

📫 Email: [ameyasabale3@gmail.com]

📎 Submission Checklist
✅ Clean folder structure
✅ All scripts documented in README
✅ Outputs zipped or uploaded to Google Drive
✅ best.pt + map.html included
✅ PDF report + screenshots optional but recommended

