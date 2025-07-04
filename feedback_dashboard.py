# dashboard_with_feedback.py (Enhanced)
import streamlit as st
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
import datetime
import uuid
import pandas as pd
from streamlit_drawable_canvas import st_canvas

# === Config ===
YOLO_MODEL_PATH = "best.pt"
CLASS_FILE = "defect_classes.txt"
IMAGE_FOLDER = "images"
ANNOTATED_FOLDER = "annotated_images"
LABEL_LOG_FILE = "label_log.csv"

os.makedirs(ANNOTATED_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

from ultralytics import YOLO
model = YOLO(YOLO_MODEL_PATH)
class_names = open(CLASS_FILE).read().splitlines()
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

if "img_index" not in st.session_state:
    st.session_state.img_index = 0
if "manual_labels" not in st.session_state:
    st.session_state.manual_labels = []

st.set_page_config(page_title="Road Defect Dashboard", layout="wide")
st.title("🚦 Smart Road Defect Labeling Dashboard")

page = st.sidebar.radio("📁 Select Page", ["🏠 Auto Labeling", "✍️ Manual Labeling", "🧾 Log"])

# === Load Images ===
image_files = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.jpg', '.png', '.jpeg'))])
if not image_files:
    st.warning("No images found in 'images/' folder.")
    st.stop()

current_image_name = image_files[st.session_state.img_index]
current_image_path = os.path.join(IMAGE_FOLDER, current_image_name)

# === Feedback Logic ===
def generate_feedback(avg_conf):
    if avg_conf >= 0.85:
        return "✅ High confidence - usable for training."
    elif avg_conf >= 0.6:
        return "⚠️ Moderate confidence - review advised."
    else:
        return "❌ Low confidence - manual labeling needed."

def generate_llm_feedback(confidence, labels, image_path):
    defects = ", ".join(sorted(set(labels))) if labels else "no defects detected"
    image_info = f"Image file: {os.path.basename(image_path)}."
    summary = f"Detected defects: {defects}.\nConfidence score: {confidence:.2f}.\n{image_info}"
    if confidence < 0.6:
        suggestion = "LLM Suggestion: Retraining or manual review recommended."
    elif confidence < 0.85:
        suggestion = "LLM Suggestion: Data might be usable after cleanup."
    else:
        suggestion = "LLM Suggestion: Good quality data for training."
    return f"🧠 LLM Feedback:\n{summary}\n{suggestion}"

# === Utility: Draw Boxes ===
def draw_boxes(image, results):
    img = image.copy()
    confidences = []
    for box in results.boxes:
        cls_id = int(box.cls.item())
        conf = float(box.conf.item())
        confidences.append(conf)
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        color = colors[cls_id % len(colors)]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, f"{class_names[cls_id]} {conf:.2f}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return img, confidences

# === Auto Labeling ===
if page == "🏠 Auto Labeling":
    st.subheader(f"📷 Auto Labeling: {current_image_name}")

    results = model.predict(current_image_path, conf=0.35, imgsz=1024, augment=True, verbose=False)[0]
    img = cv2.imread(current_image_path)
    labeled_img, confidences = draw_boxes(img, results)

    st.image(Image.fromarray(cv2.cvtColor(labeled_img, cv2.COLOR_BGR2RGB)), caption="🔍 Auto-Labeled Image")

    st.markdown("---")
    avg_conf = np.mean(confidences) if confidences else 0.0
    table_data = [[class_names[int(b.cls.item())], f"{b.conf.item():.2f}"] for b in results.boxes]
    df = pd.DataFrame(table_data, columns=["Class", "Confidence"])
    st.dataframe(df)
    st.markdown(f"### 📊 Average Confidence: `{avg_conf:.2f}`")

    st.markdown("### 🤖 Feedback Summary")
    st.info(generate_feedback(avg_conf))

    detected_classes = [class_names[int(b.cls.item())] for b in results.boxes]
    st.markdown("### 🧠 LLM Feedback")
    st.success(generate_llm_feedback(avg_conf, detected_classes, current_image_path))

    # Download button for auto-labeled image
    out_path = os.path.join(ANNOTATED_FOLDER, f"auto_{current_image_name}")
    cv2.imwrite(out_path, labeled_img)
    st.download_button("⬇️ Download Auto-Labeled Image", data=open(out_path, "rb").read(),
                       file_name=f"auto_{current_image_name}", mime="image/jpeg")

# === Manual Labeling Page ===
elif page == "✍️ Manual Labeling":
    st.subheader(f"✍️ Manual Labeling: {current_image_name}")

    image = Image.open(current_image_path).convert("RGB")
    width, height = image.size

    st.markdown("### Step 1: Select class before each box")
    current_class = st.selectbox("🎯 Defect Class", class_names)

    # Initialize box+class cache
    if "drawn_boxes" not in st.session_state:
        st.session_state.drawn_boxes = []

    base_image = image.copy()
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0.3)",
        stroke_width=2,
        stroke_color="#00ff00",
        background_image=base_image,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="rect",
        key="canvas_manual"
    )

    new_boxes = canvas_result.json_data["objects"] if canvas_result.json_data else []
    prev_count = len(st.session_state.drawn_boxes)

    if len(new_boxes) > prev_count:
        new_box = new_boxes[-1]
        st.session_state.drawn_boxes.append({
            "box": new_box,
            "class": current_class
        })

    label_data = []
    manual_classes = []
    draw_img = image.copy()
    draw = ImageDraw.Draw(draw_img)

    for item in st.session_state.drawn_boxes:
        box = item["box"]
        cls_name = item["class"]
        cls_id = class_names.index(cls_name)
        manual_classes.append(cls_name)

        left = box["left"]
        top = box["top"]
        w = box["width"]
        h = box["height"]

        x_center = (left + w / 2) / width
        y_center = (top + h / 2) / height
        w_norm = w / width
        h_norm = h / height

        label_data.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}")
        color = colors[cls_id % len(colors)]
        draw.rectangle([left, top, left + w, top + h], outline=color, width=2)
        draw.text((left, top - 10), cls_name, fill=color)

    st.image(draw_img, caption="✅ Annotated Image with Labels")

    out_path = os.path.join(ANNOTATED_FOLDER, f"manual_{current_image_name}")
    draw_img.save(out_path)

    st.download_button("⬇️ Download Annotated Image", data=open(out_path, "rb").read(),
                       file_name=f"manual_{current_image_name}", mime="image/jpeg")

    st.download_button("⬇️ Download YOLO Labels", "\n".join(label_data),
                       file_name=f"labels_{current_image_name}.txt", mime="text/plain")

    st.code("\n".join(label_data))

    st.markdown("### 🤖 Feedback Summary")
    st.info(generate_feedback(0.75))

    st.markdown("### 🧠 LLM Feedback")
    st.success(generate_llm_feedback(0.75, manual_classes, current_image_path))

# === Log Page ===
elif page == "🧾 Log":
    st.subheader("📜 Annotation Log Viewer")
    if os.path.exists(LABEL_LOG_FILE):
        df_log = pd.read_csv(LABEL_LOG_FILE)
        st.dataframe(df_log)
    else:
        st.info("No logs yet.")

# === Navigation ===
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Previous"):
        st.session_state.img_index = max(0, st.session_state.img_index - 1)
        st.experimental_rerun()
with col2:
    if st.button("➡️ Next"):
        st.session_state.img_index = min(len(image_files) - 1, st.session_state.img_index + 1)
        st.experimental_rerun()
