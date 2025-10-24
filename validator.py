import re
import spacy
import subprocess
import sys

# Try to load the spaCy model; download if missing
try:
    _nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy 'en_core_web_sm' model...")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
    _nlp = spacy.load("en_core_web_sm")


def extract_numbers(text: str):
    """Extract integers and floats from text."""
    nums = re.findall(r"[-+]?[0-9]*\.?[0-9]+", text)
    return nums


def compare_numbers(original: str, cleaned: str):
    o_nums = extract_numbers(original)
    c_nums = extract_numbers(cleaned)
    return {"original_numbers": o_nums, "cleaned_numbers": c_nums, "mismatch": o_nums != c_nums}


def extract_entities(text: str):
    doc = _nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


def compare_entities(original: str, cleaned: str):
    o_ents = extract_entities(original)
    c_ents = extract_entities(cleaned)
    return {"original_entities": o_ents, "cleaned_entities": c_ents, "mismatch": o_ents != c_ents}


def run_validations(original: str, cleaned: str):
    number_check = compare_numbers(original, cleaned)
    entity_check = compare_entities(original, cleaned)
    flag = number_check["mismatch"] or entity_check["mismatch"]
    return {"numbers": number_check, "entities": entity_check, "flag_for_review": flag}


# Optional test
if __name__ == "__main__":
    orig = "There are 42 students in Paris."
    cleaned = "There are 42 students in Paris."
    result = run_validations(orig, cleaned)
    print(result)
