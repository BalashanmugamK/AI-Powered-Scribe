import whisper


# Simple wrapper around Whisper transcription
# Note: Whisper requires ffmpeg available in PATH


def transcribe_audio(audio_path: str, whisper_model: str = "small") -> str:
"""Transcribe audio file to text using whisper."""
print(f"Loading Whisper model: {whisper_model}")
model = whisper.load_model(whisper_model)
print(f"Transcribing {audio_path}...")
result = model.transcribe(audio_path)
text = result.get("text", "").strip()
return text
