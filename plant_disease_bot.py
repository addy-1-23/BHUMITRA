import streamlit as st
import google.generativeai as genai
import base64
import requests
import imghdr
import os
import csv
from PIL import Image, ImageEnhance
from datetime import datetime

# -------------------------------
# Ensure folders exist
# -------------------------------
def ensure_directories():
    os.makedirs("data/images", exist_ok=True)
    os.makedirs("data/feedback", exist_ok=True)

ensure_directories()

# -------------------------------
# Configure Gemini API key
# -------------------------------
genai.configure(api_key="AIzaSyC7t7hp93FaziT0uOrZs7j10-cr1zcR87I")  # secure this key before deployment

# -------------------------------
# Image Functions
# -------------------------------
def download_image(image_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(image_url, headers=headers)
        if response.status_code == 200 and response.headers.get("Content-Type", "").startswith("image"):
            filename = f"data/images/url_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
        else:
            return None
    except Exception as e:
        st.error(f"❌ Error downloading image: {e}")
        return None

def detect_mime_type(file_path):
    ext = imghdr.what(file_path)
    return f"image/{ext}" if ext else "image/jpeg"

def preprocess_image(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        image = image.resize((512, 512))
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        image.save(image_path)
        return image_path
    except Exception as e:
        st.error(f"⚠️ Preprocessing error: {e}")
        return image_path

def analyze_image(image_path, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        mime_type = detect_mime_type(image_path)
        image_input = {"mime_type": mime_type, "data": base64_image}
        response = model.generate_content([prompt, image_input])
        return response.text
    except Exception as e:
        return f"🚨 Error during analysis: {e}"

# -------------------------------
# Save Feedback
# -------------------------------
def save_feedback(image_path, user_prompt, model_output, rating, user_notes, context_data):
    filename = "data/feedback/feedback_data.csv"
    headers = ["timestamp", "image_name", "prompt", "model_output", "rating", "user_notes", "plant_species", "region", "season"]
    image_name = os.path.basename(image_path)
    data = [
        datetime.now().isoformat(),
        image_name,
        user_prompt,
        model_output,
        rating,
        user_notes,
        context_data["species"],
        context_data["region"],
        context_data["season"]
    ]
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow(data)

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Plant Disease Detector 🌿", layout="centered")
st.title("🌱 BHUMITRA")
st.markdown("Upload a plant leaf image or paste a URL to analyze possible diseases.")

# --- Maintain session ---
if "result" not in st.session_state:
    st.session_state.result = None
if "image_file" not in st.session_state:
    st.session_state.image_file = None
if "prompt" not in st.session_state:
    st.session_state.prompt = None

image_file = None
input_type = st.radio("Choose image input method:", ["📤 Upload Image", "🌐 Paste Image URL"])

if input_type == "📤 Upload Image":
    uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded:
        image_file = f"data/images/{uploaded.name}"
        with open(image_file, "wb") as f:
            f.write(uploaded.read())
        st.image(image_file, caption="Uploaded Image", use_column_width=True)
        st.session_state.image_file = image_file

elif input_type == "🌐 Paste Image URL":
    url = st.text_input("Paste direct image URL here:")
    if url:
        image_file = download_image(url)
        if image_file:
            st.image(image_file, caption="Image from URL", use_column_width=True)
            st.session_state.image_file = image_file

# Context
st.markdown("### 🌿 Provide Context (optional but improves accuracy)")
species = st.text_input("Plant species (e.g., Tomato, Wheat)")
region = st.text_input("Location/Region")
season = st.selectbox("Current season", ["", "Spring", "Summer", "Monsoon", "Autumn", "Winter"])

# Prompt
default_prompt = f"""
Act as a plant pathology expert.
Step 1: Observe any visual symptoms such as color change, fungal growth, holes, or spots on the leaves.
Step 2: Compare symptoms with known plant diseases for {species or 'unknown plant'} in {region or 'any region'} during {season or 'any season'}.
Step 3: Suggest 3 most probable diseases with confidence percentages.
Step 4: Mention if diagnosis is uncertain and recommend next steps (e.g., lab testing or fungicide use).
"""
user_prompt = st.text_area("🧠 Prompt (you can modify this):", value=default_prompt, height=200)
st.session_state.prompt = user_prompt

# Analyze
if st.session_state.image_file:
    if st.button("🔍 Analyze Image"):
        preprocess_image(st.session_state.image_file)
        with st.spinner("Analyzing image ..."):
            result = analyze_image(st.session_state.image_file, st.session_state.prompt)
            st.session_state.result = result

# Show result
if st.session_state.result:
    st.markdown("### 📊 Result")
    st.success(st.session_state.result)

    # Feedback form
    with st.form("feedback_form"):
        st.markdown("### 🙋‍♂️ Rate this result")
        rating = st.radio("How accurate was the diagnosis?", ["⭐ Poor", "⭐⭐ Okay", "⭐⭐⭐ Good", "⭐⭐⭐⭐ Great", "⭐⭐⭐⭐⭐ Excellent"], key="rating")
        user_notes = st.text_area("Any suggestions or corrections?", placeholder="E.g., It missed yellow spots on the leaf...", key="notes")
        submit = st.form_submit_button("💾 Submit Feedback")
        if submit:
            context_data = {"species": species, "region": region, "season": season}
            save_feedback(
                st.session_state.image_file,
                st.session_state.prompt,
                st.session_state.result,
                rating,
                user_notes,
                context_data
            )
            st.success("✅ Feedback saved successfully!")
else:
    if st.button("🔍 Analyze Image"):
        st.warning("⚠️ Please upload an image or provide a valid image URL first.")
