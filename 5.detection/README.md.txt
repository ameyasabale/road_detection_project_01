 Detection Visualization (Frame-Based)

This module overlays defect detection results and location information directly on each image frame using the trained YOLOv12 model.

---

## 🎯 Purpose

After performing detection and reverse geocoding in Step 4, this step:

- Loads each extracted frame from the video
- Runs YOLOv12 detection (`best.pt`) to identify road defects
- Retrieves the real-world location from the CSV
- Draws:
  - 🔲 Bounding boxes for each detected object
  - 📍 Location (city/state) at the top of the image
  - 🧮 Running count of each detected class (live summary)
- Displays the frame in a popup window (`OpenCV`)
- Saves the final labeled image to disk

---

## 📥 Input

- **Frame Images**  
  Location:
C:/Users/M.P/Downloads/frames_all1/extracted_frames/

vbnet
Copy
Edit

- **final_output1.csv**  
From Step 4 — contains frame names, lat/lon, and geocoded location  
Location:
C:/Users/M.P/Downloads/road_project_final/final_output1.csv

markdown
Copy
Edit

✅ Expected columns:
- `Frame`
- `Latitude`
- `Longitude`
- `Location`
- `Defect Categories`
- `Total Defects`

- **Trained YOLOv12 Model**
File:
best.pt

yaml
Copy
Edit

> ⚠️ This file is large and should be uploaded to Google Drive —  
> 📎 [Download `best.pt` from here](https://drive.google.com/your-link-here)

---

## 📤 Output

- **Saved labeled frames folder**  
All processed frames with boxes + overlays are saved to:
C:/Users/M.P/Downloads/output03/

yaml
Copy
Edit

- **Live Preview Window**  
You can see the labeled images as they’re being processed.

- **Final Detection Summary**  
Total number of each defect category printed in terminal.

---

## ▶️ How to Run

Make sure Python, OpenCV, pandas, and ultralytics YOLO are installed.

```bash
python visualize_frames_with_location.py
✅ Press ESC anytime to stop early
✅ All images until that point will still be saved

🛠 Customization
Adjust image display speed:

python
Copy
Edit
key = cv2.waitKey(300) & 0xFF  # 300 ms delay (3 fps)
Resize image dimensions:

python
Copy
Edit
frame = cv2.resize(frame, (1020, 600))
Modify box colors per class:

python
Copy
Edit
color = (0, 255, 0) if label.lower() == 'pothole' else (255, 255, 0)
✅ Example Output (frame_0012.jpg)
pgsql
Copy
Edit
+--------------------------------------------------------+
| Location: Pune, Maharashtra, India                    |
| Pothole: 2                                             |
| Damage Surface: 1                                      |
|                                                        |
|   [🔲 Bounding boxes with class labels on road image]   |
+--------------------------------------------------------+
📁 Folder Structure
bash
Copy
Edit

detection/
├── visualize_frames_with_location.py     # Live overlay + save script
├── final_output1.csv                     # Input from Step 4
├── labelled_frames/                      # (Optional) if you're storing outputs here
└── README.md                             # This file
📌 Dependencies
Install required libraries if not already installed:

bash
Copy
Edit
pip install ultralytics opencv-python pandas
