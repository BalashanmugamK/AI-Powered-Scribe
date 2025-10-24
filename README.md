# 🧠 AI-Powered Scribe: Assistive Answer Recording for Specially-Abled Students

## 🎯 Objective

The **AI-Powered Scribe** assists visually impaired or specially-abled students during verbal answering by converting speech into clean, readable text. Its primary function is to remove **disfluencies** (like "uh," "um," repetitions) without altering any factual content, ensuring a fair and accurate transcript of the student's knowledge.

## 🏗️ System Workflow

The process is designed for high integrity and accuracy:

1. **Question is Read:** Question is read aloud or accessed via a screen reader.

2. **Student Speaks:** Student records their verbal answer.

3. **STT Transcription:** **Speech-to-Text (STT)** module transcribes the audio response (using Whisper).

4. **AI Cleaning:** The **AI Cleaner** (powered by Gemini) removes fillers and repetitions. **No factual changes are permitted.**

5. **Safety Validation:** A **Safety Validator** ensures that the original meaning, numbers, and facts are perfectly preserved.

6. **Final Output:** The cleaned transcript is saved/submitted as the student’s final answer.

## 🧩 Tech Stack

| Component | Technology | Role | 
 | ----- | ----- | ----- | 
| **Speech Recognition** | **Whisper / Python SpeechRecognition** | Converts audio to raw text transcript. | 
| **Disfluency Cleaner** | **Gemini API (Google Generative AI)** | Removes filler words and repetitions using a precise prompt. | 
| **Validation Layer** | **Python (regex + spaCy)** | Ensures facts, numbers, and named entities remain completely unchanged. | 
| **Frontend / UI** | **Streamlit** | Provides an accessible, interactive web interface. | 
| **Deployment** | **Docker / Streamlit** | Facilitates portable local or web app deployment. | 

## 🗂️ Folder Structure

    AI-Powered-Scribe/
    ├── app.py              # Streamlit UI interface
    ├── cleaner.py          # Gemini-based disfluency cleaner module
    ├── stt.py              # Speech-to-text integration using Whisper
    ├── validator.py        # Validates cleaned vs original text integrity
    ├── requirements.txt    # Project dependencies
    ├── README.md           # Project documentation
    ├── data/
    │   ├── samples/        # Sample audio files for testing
    │   └── outputs/        # Cleaned output transcripts
    ├── assets/
    │   ├── icon.png        # Optional logo
    │   └── banner.jpg      # Optional banner image
    └── .env                # Optional: Holds the Gemini API key


## ⚙️ Setup Instructions

### Step 1 — Clone or Create Folder



mkdir AI-Powered-Scribe
cd AI-Powered-Scribe


### Step 2 — Create Virtual Environment



python -m venv venv
venv\Scripts\activate # Windows

OR

source venv/bin/activate # macOS/Linux


### Step 3 — Install Dependencies

Install all necessary packages from the requirements file:



pip install -r requirements.txt


### Step 4 — Configure API Key

Create a **`.env`** file in the root directory or paste the key directly into the Streamlit sidebar when running the app:



GENAI_API_KEY=your_google_generative_ai_key_here


### Step 5 — Run the App

Start the accessible web interface:



streamlit run app.py


## 🧠 Features

* **Real-time Speech-to-Text:** Utilizes **Whisper** for accurate, multi-language transcription.

* **AI-Powered Cleaning:** Uses **Gemini 2.0 Flash** for highly effective filler word and repetition removal.

* **Strict Factual Preservation:** Validation layer ensures *zero change* to meaning, numbers, or factual content.

* **Auditability:** Uses a **JSON-based deterministic output** for easy auditing and verification.

* **Accessible Interface:** **Streamlit** provides an interface with strong keyboard and screen-reader support.

* **Deterministic LLM Settings:** **`temperature = 0`** and **`response_mime_type = "application/json"`** enforce reproducible, predictable, and strictly formatted output.

## 🧪 Example Input & Output

This demonstrates the core functionality of removing disfluencies while preserving the core message.

### Raw Speech Transcript:

> “Okay so um hi yeah today I’m gonna uh talk about the uh water cycle I think yeah.”

### Cleaned Output:

> “Okay, hi! Today I’m going to talk about the water cycle, I think.”

### Edits Made:

* Removed fillers: `um`, `uh`, `yeah`.

* Fixed punctuation and capitalization for readability.

* **Crucially, the factual content and meaning were preserved.**

## 🚀 Future Improvements

* Integrate `streamlit-webrtc` for native, in-browser microphone recording.

* Develop an offline disfluency cleaner (e.g., using spaCy + rule-based methods) for reduced latency.

* Enhance multilingual transcription and cleaning capabilities.

* Add an optional **text summarization** feature for summarizing very long answers.

* Optimize deployment via Docker or cloud platforms for simplified, universal access.
