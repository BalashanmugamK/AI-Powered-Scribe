import whisper

# Simple wrapper around Whisper transcription
# Make sure ffmpeg is installed and available in PATH


def transcribe_audio(audio_path: str, whisper_model: str = "small") -> str:
    """
    Transcribe audio file to text using Whisper.
    Returns the transcription as a string.
    """
    print(f"Loading Whisper model: {whisper_model}...")
    model = whisper.load_model(whisper_model)
    print(f"Transcribing audio: {audio_path} ...")
    result = model.transcribe(audio_path)
    text = result.get("text", "").strip()
    return text


# Optional test block
if __name__ == "__main__":
    sample_audio = "data/samples/sample.wav"  # replace with your test audio file path
    transcription = transcribe_audio(sample_audio)
    print("Transcription:", transcription)
