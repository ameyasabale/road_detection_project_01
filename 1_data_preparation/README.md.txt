# 1. Data Preparation – Frame Extraction

This folder contains the script used to extract image frames from a video for training and analysis.

---

## 🧾 Files
- `frame_extraction.py`: Python script that extracts frames at 2 frames per second.
- `extracted_frames/`: Output folder where the extracted `.jpg` images are saved.
- `sample_video.mp4`: (Optional) A sample road video from which frames are extracted.

---

## ⚙️ How it Works
- The script reads a video file (`.mp4`)
- Extracts frames at regular intervals (2 FPS)
- Saves each frame as a `.jpg` in the `extracted_frames/` folder

---

## ▶️ How to Run

1. Make sure Python and OpenCV are installed:
