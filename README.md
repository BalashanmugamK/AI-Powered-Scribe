🧠 AI-Powered Scribe: Assistive Answer Recording for Specially-Abled Students
🎯 Objective

The AI-Powered Scribe assists visually impaired or specially-abled students during verbal answering by converting speech into clean, readable text.
It removes disfluencies (like “uh”, “um”, repetitions) without altering any factual content.

🏗️ System Workflow

1️⃣ Question is read aloud or accessed via screen reader
2️⃣ Student speaks their answer
3️⃣ Speech-to-Text (STT) module transcribes the response
4️⃣ AI Cleaner removes fillers and repetitions (no factual changes)
5️⃣ Safety Validator ensures meaning, numbers, and facts are preserved
6️⃣ Cleaned transcript is saved/submitted as the student’s final answer

🧩 Tech Stack

Speech Recognition: Whisper / Python SpeechRecognition → Converts audio to text

Disfluency Cleaner: Gemini API (Google Generative AI) → Removes fillers & repetitions

Validation Layer: Python (regex + spaCy) → Ensures facts, numbers, entities remain unchanged

Frontend / UI: Streamlit → Accessible web interface

Deployment: Docker / Streamlit → Portable local or web app

🗂️ Folder Structure

AI-Powered-Scribe/
├── app.py # Streamlit UI
├── cleaner.py # Gemini-based disfluency cleaner
├── stt.py # Speech-to-text using Whisper
├── validator.py # Validates cleaned vs original text
├── requirements.txt # Dependencies
├── README.md # Project documentation
├── data/
│ ├── samples/ # Sample audio files
│ └── outputs/ # Cleaned output transcripts
├── assets/
│ ├── icon.png # Optional logo
│ └── banner.jpg # Optional banner
└── .env # Optional Gemini API key

⚙️ Setup Instructions

Step 1 — Clone or Create Folder

mkdir AI-Powered-Scribe
cd AI-Powered-Scribe


Step 2 — Create Virtual Environment

python -m venv venv
venv\Scripts\activate        # Windows
# or
source venv/bin/activate     # macOS/Linux


Step 3 — Install Dependencies

pip install -r requirements.txt


Step 4 — Configure API Key
Create a .env file or paste key in Streamlit sidebar:

GENAI_API_KEY=your_google_generative_ai_key_here


Step 5 — Run the App

streamlit run app.py

🧠 Features

Real-time Speech-to-Text (multi-language via Whisper)

AI-powered filler word removal (Gemini 2.0 Flash)

Strict factual preservation (no meaning or number changes)

JSON-based deterministic output for auditability

Human-verifiable validation layer

Accessible Streamlit interface (keyboard/screen-reader support)

🧪 Example Input & Output

Raw Speech Transcript:

“Okay so um hi yeah today I’m gonna uh talk about the uh water cycle I think yeah.”

Cleaned Output:

“Okay, hi! Today I’m going to talk about the water cycle, I think.”

Edits Made:

Removed fillers: um, uh, yeah

Fixed punctuation and capitalization

Preserved meaning and factual content

🔐 Deterministic LLM Settings

temperature = 0 → ensures reproducible output

response_mime_type = "application/json" → enforces strict JSON format

Validator checks numbers and named entities to prevent silent factual changes

🚀 Future Improvements

Integrate streamlit-webrtc for in-browser microphone recording

Add offline disfluency cleaner (spaCy + rule-based)

Enable multilingual transcription

Add text summarization for long answers

Deploy via Docker or cloud platforms for easy access
