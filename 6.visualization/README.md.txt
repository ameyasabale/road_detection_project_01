 Interactive GPS Defect Map

This module visualizes the road defects detected using YOLOv12 on an interactive map using the `folium` library.

It uses GPS coordinates (Latitude, Longitude) from the detection results and displays them as markers with detailed popups.

---

## 🎯 Purpose

- Show geolocated markers for every detected road defect
- Visually analyze defect locations on a real-world map
- View popup info including defect types, frame name, and location
- Enable route-based analysis of defect spread

---

## 📥 Input

- `final_output1.csv`  
  File generated in **Step 4** that contains the defect detection results and reverse-geocoded locations.

  ✅ Expected columns:
  - `Frame`
  - `Latitude`
  - `Longitude`
  - `Location`
  - `Defect Categories`
  - `Total Defects`

  📍 Example location:


📌 Dependencies
Install required packages with:

bash
Copy
Edit
pip install folium pandas
