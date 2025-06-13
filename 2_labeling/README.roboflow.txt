 Labeling (Roboflow Annotation & Dataset Export)

This module covers the **image labeling and dataset preparation step** using [Roboflow](https://roboflow.com/). It includes exporting annotations in YOLOv12 format and organizing them for training.

---

## 🎯 Purpose

- Label extracted frames with road defect categories (e.g., pothole, cracks, damage surface)
- Export the dataset in YOLOv12 format compatible with Ultralytics
- Convert any non-JPG images (PNG, JPEG) to `.jpg` if needed
- Prepare the dataset structure for training in Step 3

---

## 🧠 Tools Used

- ✅ Roboflow for image annotation and dataset versioning
- ✅ Python (`PIL`, `os`, `cv2`) for image format conversion

---

## 📥 Input

- **Images from Step 1**  
  Located in:
