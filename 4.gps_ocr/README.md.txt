# 4. GPS OCR + Geolocation + Defect Detection

This step processes the extracted video frames and adds geographical intelligence and defect details.

---

## 📍 1. GPS Extraction

Folder: `1_gps_extraction/`

- Uses Tesseract OCR to extract Latitude and Longitude from each frame.
- Output: `gps_from_frames.csv`

---

## 🧠 2. Defect Detection + Location Mapping

Folder: `2_detection_and_geocoding/`

- Uses YOLO (`best.pt`) to detect defects in frames
- Uses lat/lon from `gps_from_frames.csv`
- Applies reverse geocoding to extract city/state/country
- Adds total and unique defect category count per frame
- Output: `final_output.csv`

---

## 🔧 Run Instructions

```bash
cd 4_gps_ocr/1_gps_extraction
python extract_gps_from_frames.py

cd ../2_detection_and_geocoding
python detect_and_geocode.py
