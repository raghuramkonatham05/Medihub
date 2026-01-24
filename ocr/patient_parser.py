# ocr/patient_parser.py
import re


def extract_patient_info(text):
    """
    Robust patient info extractor for Indian lab reports.
    Works across different hospital formats.
    """

    info = {
        "name": "Patient",
        "age": "--",
        "gender": "Unknown"
    }

    if not text:
        return info

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    joined = " ".join(lines)

    # -------------------------------
    # NAME EXTRACTION
    # -------------------------------
    name_patterns = [
        r"(?:name|pt name|patient name)\s*[:\-]?\s*([A-Z][A-Za-z .]+)",
        r"\bMr\.?\s+([A-Z][A-Za-z .]+)",
        r"\bMrs\.?\s+([A-Z][A-Za-z .]+)",
        r"\bMs\.?\s+([A-Z][A-Za-z .]+)",
    ]

    for pat in name_patterns:
        m = re.search(pat, joined, re.IGNORECASE)
        if m:
            info["name"] = m.group(1).strip().title()
            break

    # -------------------------------
    # AGE & GENDER (COMBINED)
    # -------------------------------
    age_gender_patterns = [
        r"age\s*/\s*gender\s*[:\-]?\s*(\d{1,3})\s*/\s*([MF])",
        r"age\s*[:\-]?\s*(\d{1,3}).{0,10}sex\s*[:\-]?\s*([MF])",
        r"sex\s*/\s*age\s*[:\-]?\s*([MF]).{0,10}(\d{1,3})",
    ]

    for pat in age_gender_patterns:
        m = re.search(pat, joined, re.IGNORECASE)
        if m:
            if m.group(1).isdigit():
                info["age"] = m.group(1)
                info["gender"] = "Male" if m.group(2).upper() == "M" else "Female"
            else:
                info["age"] = m.group(2)
                info["gender"] = "Male" if m.group(1).upper() == "M" else "Female"
            break

    # -------------------------------
    # AGE ONLY (fallback)
    # -------------------------------
    if info["age"] == "--":
        age_match = re.search(r"\b(\d{1,3})\s*(?:years|yrs|year)\b", joined, re.IGNORECASE)
        if age_match:
            info["age"] = age_match.group(1)

    # -------------------------------
    # GENDER ONLY (fallback)
    # -------------------------------
    if info["gender"] == "Unknown":
        if re.search(r"\bmale\b|\bsex\s*[:\-]?\s*m\b", joined, re.IGNORECASE):
            info["gender"] = "Male"
        elif re.search(r"\bfemale\b|\bsex\s*[:\-]?\s*f\b", joined, re.IGNORECASE):
            info["gender"] = "Female"

    print("🧍 PATIENT INFO:", info)
    return info
