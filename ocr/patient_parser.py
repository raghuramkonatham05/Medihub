import re


def extract_patient_info(text):
    """
    Robust patient info extractor for Indian lab reports.
    Handles:
    - Same-line & multi-line layouts
    - Initials (G. Nagi Reddy)
    - Name on next line after 'Name'
    - Age/Gender split across lines
    - Formats:
        Age : 49 Sex : M
        49 / M
        Male / 40 Years
    - Removes OCR junk (0, Date, Age, Sex, etc.)
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

    # =====================================================
    # 1️⃣ NAME EXTRACTION (LINE + NEXT LINE)
    # =====================================================
    for i, line in enumerate(lines):

        # Case: "Name" on one line, value on next
        if re.fullmatch(r"(name|patient\s*name)", line, re.IGNORECASE):
            if i + 1 < len(lines):
                candidate = lines[i + 1]

                if len(candidate) > 2 and not candidate.isdigit():
                    info["name"] = candidate.title()
                    break

        # Case: Name : Value
        m = re.search(
            r"(?:pt\.?\s*name|patient\s*name|name)\s*[:\-]?\s*([A-Z][A-Za-z.\s]+)",
            line,
            re.IGNORECASE
        )
        if m:
            name = m.group(1)

            # Remove trailing junk
            name = re.sub(
                r"\b(date|age|sex|specimen|doctor|ref)\b.*$",
                "",
                name,
                flags=re.IGNORECASE
            )

            if len(name) > 2 and not name.isdigit():
                info["name"] = name.strip().title()
                break

    # =====================================================
    # 2️⃣ NAME FALLBACK (INITIALS ANYWHERE)
    # =====================================================
    if info["name"] == "Patient":
        m = re.search(
            r"\b(?:Mr|Mrs|Ms)?\s*(?:[A-Z]\.\s*)*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+",
            joined
        )
        if m:
            info["name"] = m.group(0).strip().title()

    # =====================================================
    # 3️⃣ MULTI-LINE SEX / AGE
    # =====================================================
    for i, line in enumerate(lines):
        if re.search(r"sex\s*/?\s*age", line, re.IGNORECASE):
            # Gender on next line
            if i + 1 < len(lines):
                g = lines[i + 1].lower()
                if "male" in g or g == "m":
                    info["gender"] = "Male"
                elif "female" in g or g == "f":
                    info["gender"] = "Female"

            # Age on next-next line
            if i + 2 < len(lines):
                m = re.search(r"(\d{1,3})", lines[i + 2])
                if m:
                    info["age"] = m.group(1)
            break

    # =====================================================
    # 4️⃣ SAME-LINE AGE + GENDER FORMATS
    # =====================================================
    age_gender_patterns = [
        r"age\s*[:\-]?\s*(\d{1,3})\s*sex\s*[:\-]?\s*([mf])",
        r"age\s*[:\-]?\s*(\d{1,3}).{0,10}?\b([mf])\b",
        r"(\d{1,3})\s*/\s*([mf])",
        r"(male|female)\s*/\s*(\d{1,3})\s*years"
    ]

    for pat in age_gender_patterns:
        m = re.search(pat, joined, re.IGNORECASE)
        if m:
            if m.group(1).lower() in ["male", "female"]:
                info["gender"] = m.group(1).title()
                info["age"] = m.group(2)
            else:
                info["age"] = m.group(1)
                info["gender"] = "Male" if m.group(2).upper() == "M" else "Female"
            break

    # =====================================================
    # 5️⃣ FINAL FALLBACKS
    # =====================================================
    if info["age"] == "--":
        m = re.search(r"\b(\d{1,3})\s*years\b", joined, re.IGNORECASE)
        if m:
            info["age"] = m.group(1)

    if info["gender"] == "Unknown":
        if re.search(r"\bmale\b", joined, re.IGNORECASE):
            info["gender"] = "Male"
        elif re.search(r"\bfemale\b", joined, re.IGNORECASE):
            info["gender"] = "Female"

    print("🧍 PATIENT INFO:", info)
    return info
