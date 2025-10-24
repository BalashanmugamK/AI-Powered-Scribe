import streamlit as st
from cleaner import clean_text
from validator import run_validations


st.set_page_config(page_title="AI-Powered Scribe", layout="centered")


st.title("AI-Powered Scribe — Assistive Answer Recording")
st.markdown("Upload an audio file (mp3/wav/m4a). The app transcribes using Whisper, cleans disfluencies using Gemini, and validates for factual drift.")


# Sidebar: API key and settings
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("GENAI API Key", type="password")
whisper_model = st.sidebar.selectbox("Whisper model", ["small", "base", "medium"], index=0)


if api_key:
os.environ["GENAI_API_KEY"] = api_key


uploaded_file = st.file_uploader("Upload audio file (mp3/wav/m4a)", type=["mp3", "wav", "m4a", "ogg"])


if uploaded_file is not None:
# Save temporarily
tmp_path = "tmp_uploaded_audio"
with open(tmp_path, "wb") as f:
f.write(uploaded_file.getbuffer())


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


# Download buttons
cleaned_text = cleaned.get("cleaned", cleaned.get("original", ""))
b64 = base64.b64encode(cleaned_text.encode()).decode()
href = f"data:file/text;base64,{b64}"
st.markdown(f"[Download cleaned answer](%s)" % href)


# JSON download
json_b64 = base64.b64encode(json.dumps(cleaned, ensure_ascii=False, indent=2).encode()).decode()
st.markdown(f"[Download JSON result](data:application/json;base64,{json_b64})")
