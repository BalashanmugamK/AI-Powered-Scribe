import json
import google.generativeai as genai
import os


# Configure via environment variable: GENAI_API_KEY
_genai_key = os.getenv("GENAI_API_KEY")
if not _genai_key:
raise EnvironmentError("Please set the GENAI_API_KEY environment variable.")


genai.configure(api_key=_genai_key)
_model = genai.GenerativeModel("gemini-2.0-flash")




def _extract_json(text: str):
"""Robust JSON extractor with fallback"""
try:
return json.loads(text)
except Exception:
pass


try:
start = text.find("{")
end = text.rfind("}")
if start != -1 and end != -1 and end > start:
return json.loads(text[start:end+1])
except Exception:
return {"original": None, "cleaned": text.strip(), "edits": ["(parser fallback)"]}




def clean_text(raw: str):
"""Call Gemini to remove disfluencies but preserve facts. Returns dict with original, cleaned, edits."""
system_rules = r"""
CRITICAL INSTRUCTION: You are a linguistic cleaner with ONE JOB ONLY:


REMOVE ONLY THESE DISFLUENCIES:
- Filler words: "uh", "um", "like", "you know", "basically", "stuff", "or something"
- Stammers and word repetitions that are clearly speech errors
- Fix basic punctuation, capitalization, spacing


ABSOLUTE PROHIBITIONS - NEVER DO THESE UNDER ANY CIRCUMSTANCES:
❌ NEVER change any factual claims, even if they are obviously wrong
❌ NEVER swap, correct, or "fix" named entities (people, places, organizations)
❌ NEVER change numbers, dates, quantities, or measurements
❌ NEVER add missing information or infer what the speaker "meant"
❌ NEVER correct historical facts, scientific facts, or any factual errors
❌ NEVER change the meaning or substance of what was said


Your job is to make speech readable, NOT to make it correct.


Output format: JSON only
{
"original": "<exact input>",
"cleaned": "<cleaned version with NO factual changes>",
"edits": ["<list of ONLY linguistic edits made>"]
}
"""


# short examples (shots) to increase reliability
shots = [
{
"in": "uh the capital of France is Berlin I think um yeah Berlin.",
"out": {
"cleaned": "The capital of France is Berlin, I think—yeah, Berlin.",
return parsed
