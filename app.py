import os
import json
import base64
import tempfile
import streamlit as st
from dotenv import load_dotenv

# For in-browser mic recording
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import numpy as np
import soundfile as sf

# Load environment variables from .env (for local testing)
load_dotenv()

from cleaner import clean_text
from validator import run_validations
from stt import transcribe_audio  # Ensure stt.py exists with transcribe_audio function

# -------------------
# Streamlit page config
# -------------------
st.set_page_config(page_title="AI-Powered Scribe", layout="centered")

st.title("AI-Powered Scribe — Assistive Answer Recording")
st.markdown(
    "Upload an audio file (mp3/wav/m4a/ogg) or record directly from your browser. "
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

# -------------------
# Microphone recorder
# -------------------
st.subheader("🎤 Record audio using your microphone")

class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.audio_buffer = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio_np = frame.to_ndarray()
        self.audio_buffer.append(audio_np)
        return frame

    def get_audio(self):
        if not self.audio_buffer:
            return None
        audio_data = np.concatenate(self.audio_buffer, axis=1).T
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        sf.write(tmp_file.name, audio_data, 48000)  # 48 kHz
        return tmp_file.name

recorder = webrtc_streamer(
    key="mic",
    audio_processor_factory=AudioRecorder,
    media_stream_constraints={"audio": True, "video": False},
)

# -------------------
# Processing function
# -------------------
def process_audio_file(tmp_path):
    st.audio(tmp_path)
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

# -------------------
# File uploader button
# -------------------
if uploaded_file is not None:
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp_file.write(uploaded_file.getbuffer())
    tmp_path = tmp_file.name
    tmp_file.close()

    if st.button("Transcribe and Clean Uploaded Audio"):
        process_audio_file(tmp_path)

# -------------------
# Microphone button
# -------------------
if st.button("Transcribe Recorded Audio"):
    if recorder.audio_processor:
        audio_file_path = recorder.audio_processor.get_audio()
        if audio_file_path:
            process_audio_file(audio_file_path)
        else:
            st.warning("No audio recorded yet!")
