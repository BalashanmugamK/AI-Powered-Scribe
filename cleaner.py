import json
import os
import streamlit as st
import google.generativeai as genai

# -------------------
# API Key Handling
# -------------------
# First, try to get key from Streamlit secrets
api_key = st.secrets.get("genai", {}).get("GENAI_API_KEY") if "st" in globals() else None

# Fallback: use environment variable (or .env locally)
if not api_key:
    api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    raise EnvironmentError(
        "GENAI_API_KEY not found! Set it in Streamlit secrets or as an environment variable."
    )

# Configure Gemini API
genai.configure(api_key=api_key)
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
            return json.loads(text[start:end + 1])
    except Exception:
        pass

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
                "edits": [
                    "Removed fillers: 'uh', 'um'",
                    "Fixed capitalization and punctuation",
                    "PRESERVED factual claim 'Berlin' (even though incorrect)"
                ]
            }
        },
        {
            "in": "um Lincoln was assassinated by um John Wilkes Booth in like 1900 I think.",
            "out": {
                "cleaned": "Lincoln was assassinated by John Wilkes Booth in 1900, I think.",
                "edits": [
                    "Removed fillers: 'um', 'like'",
                    "Fixed punctuation",
                    "PRESERVED incorrect date '1900' without correction"
                ]
            }
        }
    ]

    exemplar_blocks = []
    for s in shots:
        exemplar_blocks.append(
            f'Input:\n{s["in"]}\n\nRequired Output:\n' +
            json.dumps({"original": s["in"], **s["out"]}, ensure_ascii=False, indent=2)
        )
    exemplars = "\n\n---\n\n".join(exemplar_blocks)

    prompt = f"""{system_rules}

STUDY THESE EXAMPLES - NOTICE HOW FACTUAL ERRORS ARE PRESERVED:
{exemplars}

REMEMBER: Your job is linguistic cleaning only. DO NOT be helpful by fixing facts.
If you change any factual content, you have failed completely.

Now process this input:

Input:
{raw}

Return JSON only:"""

    try:
        resp = _model.generate_content(
            prompt,
            generation_config={
                "temperature": 0,
                "top_p": 0.1,
                "candidate_count": 1,
                "max_output_tokens": 1024,
                "response_mime_type": "application/json"
            }
        )
        parsed = _extract_json(resp.text)
    except Exception as e:
        return {
            "original": raw,
            "cleaned": raw,
            "edits": [f"API error: {str(e)}"]
        }

    if not isinstance(parsed, dict):
        parsed = {"original": raw, "cleaned": resp.text.strip(), "edits": ["(non-dict response)"]}

    parsed.setdefault("original", raw)
    parsed.setdefault("cleaned", raw)
    parsed.setdefault("edits", [])

    return parsed


# -------------------
# Test block
# -------------------
if __name__ == "__main__":
    sample = "Uh hi, so um today I will talk about the water cycle."
    print(json.dumps(clean_text(sample), indent=2, ensure_ascii=False))
