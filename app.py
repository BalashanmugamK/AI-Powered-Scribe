import os
import json
import base64
import tempfile
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env (for local testing)
load_dotenv()

from cleaner import clean_text
from validator import run_validations
from stt import transcribe_audio  # Ensure stt.py exists with transcribe_audio function

# Streamlit page config
st.set_page_config(page_title="AI-Powered Scribe", layout="centered")

st.title("AI-Powered Scribe — Assistive Answer Recording")
st.markdown(
    "Upload an audio file (mp3/wav/m4a/ogg). "
    "The app transcribes using Whisper, cleans disfluencies using Gemini, "
    "and validates for factual drift."
)

# -------------------
# Sidebar settings
# -------------------
st.sidebar.header("Configuration")

# Whisper model selection
whisper_model = st.sidebar.selectbox("Whisper model", ["small", "base", "medium"], index=0)

# -------------------
# API key handling
# -------------------
# First, try to get key from Streamlit secrets
api_key = st.secrets.get("genai", {}).get("GENAI_API_KEY")

# Fallback: use .env for local testing
if not api_key:
    api_key = os.getenv("GENAI_API_KEY")

# Set the API key in environment variable
if api_key:
    os.environ["GENAI_API_KEY"] = api_key
else:
    st.warning("⚠️ No GENAI API Key found! Please add it in Streamlit secrets.")

# -------------------
# File uploader
# -------------------
uploaded_file = st.file_uploader(
    "Upload audio file (mp3/wav/m4a/ogg)", type=["mp3", "wav", "m4a", "ogg"]
)

if uploaded_file is not None:
    # Save temporarily with a unique file name
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp_file.write(uploaded_file.getbuffer())
    tmp_path = tmp_file.name
    tmp_file.close()

    st.audio(tmp_path)

    if st.button("Transcribe and Clean"):
        with st.spinner("Transcribing with Whisper..."):
            transcript = transcribe_audio(tmp_path, whisper_model=whisper_model)

        st.subheader("Raw Transcription")
        st.write(transcript)

        with st.spinner("Cleaning with Gemini..."):
            cleaned = clean_text(transcript)

        st.subheader("Cleaned Output (JSON)")
        st.json(cleaned)

        with st.spinner("Running validations..."):
            validations = run_validations(cleaned["original"], cleaned["cleaned"])

        st.subheader("Validation Report")
        st.json(validations)

        if validations.get("flag_for_review"):
            st.warning("⚠️ Validation mismatch detected. Please review before submitting.")
        else:
            st.success("✅ No mismatches detected.")

        # Download cleaned text
        cleaned_text = cleaned.get("cleaned", cleaned.get("original", ""))
        b64 = base64.b64encode(cleaned_text.encode()).decode()
        href = f"data:file/text;base64,{b64}"
        st.markdown(f"[Download cleaned answer]({href})")

        # Download JSON
        json_b64 = base64.b64encode(
            json.dumps(cleaned, ensure_ascii=False, indent=2).encode()
        ).decode()
        st.markdown(f"[Download JSON result](data:application/json;base64,{json_b64})")
