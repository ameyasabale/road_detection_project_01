 Reports & Results

This module contains the final reports and summaries generated from the complete defect detection pipeline. It includes detection statistics, sample outputs, metadata reports, and all supporting documents required for evaluation or submission.

---

## 🎯 Purpose

- Present detection results in readable formats (CSV, Excel, PDF, visuals)
- Share analysis based on defect counts, locations, and types
- Document model performance and GPS-based insights
- Package all results in one place for easy sharing or evaluation

---

## 📥 Input Sources

- `final_output1.csv`  
  Comes from Step 4 (YOLO + GPS + Location detection)

- Labeled output frames  
  From Step 5: `5_detection/output03/`

- Optional: Map file  
  From Step 6: `6_visualization/map.html`

---

## 📤 Contents of This Folder

| File / Folder               | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| `final_output1.csv`         | Master report with Frame, Lat, Lon, Location, Defects                      |
| `defect_summary.csv`        | Class-wise count of defects detected                                       |
| `sample_frames/`            | Folder of selected labeled images with various defects                     |
| `map.html` (optional)       | Interactive map from Step 6 showing defect positions                       |
| `report.pdf` (optional)     | Final compiled report for presentation or submission                       |

---

## ✅ Example: `defect_summary.csv`

