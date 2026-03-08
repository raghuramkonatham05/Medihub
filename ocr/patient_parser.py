import re


def extract_patient_info(text):
    info = {
        "name": "Patient",
        "age": "--",
        "gender": "Unknown"
    }

    if not text:
        return info

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    joined = " ".join(lines)

    # --------------------------------------------------
    # BLOCK WORDS (NEVER A PERSON NAME)
    # --------------------------------------------------
    BLOCK_WORDS = {
        "diagnostic", "laboratory", "hospital", "centre", "center",
        "clinic", "pathology", "blood", "specimen",
        "nagar", "road", "street", "lane", "district",
        "mandal", "state", "rajamahendravaram"
    }

    def clean(text):
        return re.sub(r"[^A-Za-z.\s]", "", text).strip()

    def is_valid_name(name):
        words = name.split()
        if not (2 <= len(words) <= 4):
            return False
        if any(w.lower() in BLOCK_WORDS for w in words):
            return False
        if re.search(r"\d", name):
            return False
        return True

    # ==================================================
    # 1️⃣ NAME (LABEL + FORWARD SCAN)
    # ==================================================
    for i, line in enumerate(lines):
        if re.fullmatch(r"(name|patient\s*name)", line, re.IGNORECASE):
            for j in range(i + 1, min(i + 6, len(lines))):
                candidate = clean(lines[j])
                if candidate.lower() in {"", "0", "o"}:
                    continue
                if is_valid_name(candidate):
                    info["name"] = candidate.replace(".", ". ").title()
                    break
            break

        m = re.search(
            r"(?:name|patient\s*name)\s*[:\-]?\s*([A-Za-z.\s]{5,})",
            line,
            re.IGNORECASE
        )
        if m:
            candidate = clean(m.group(1))
            if is_valid_name(candidate):
                info["name"] = candidate.replace(".", ". ").title()
                break

    # ==================================================
    # 2️⃣ CONTEXTUAL FALLBACK (NEAR AGE / SEX ONLY)
    # ==================================================
    if info["name"] == "Patient":
        for i, line in enumerate(lines):
            if re.search(r"\b(age|sex|gender)\b", line, re.IGNORECASE):
                for back in lines[max(0, i - 5):i][::-1]:
                    candidate = clean(back)
                    if is_valid_name(candidate):
                        info["name"] = candidate.replace(".", ". ").title()
                        break
            if info["name"] != "Patient":
                break

    # ==================================================
    # 3️⃣ AGE EXTRACTION (ALL FORMATS)
    # ==================================================
    m = re.search(r"\bage\s*[:\-]?\s*(\d{1,3})\b", joined, re.IGNORECASE)
    if not m:
        m = re.search(r"\b(\d{1,3})\s*(years|yrs)\b", joined, re.IGNORECASE)
    if not m:
        m = re.search(r"\b(\d{1,3})\s*/\s*(m|f)\b", joined, re.IGNORECASE)

    if m:
        info["age"] = m.group(1)

    # ==================================================
    # 4️⃣ GENDER EXTRACTION (FIXED ✅)
    # ==================================================

    # Sex: M / F
    m = re.search(r"\bsex\s*[:\-]?\s*(m|f)\b", joined, re.IGNORECASE)
    if m:
        info["gender"] = "Male" if m.group(1).lower() == "m" else "Female"
    else:
        # AGE / GENDER : 65 /F
        m = re.search(r"\b\d{1,3}\s*/\s*(m|f)\b", joined, re.IGNORECASE)
        if m:
            info["gender"] = "Male" if m.group(1).lower() == "m" else "Female"
        else:
            if re.search(r"\bmale\b", joined, re.IGNORECASE):
                info["gender"] = "Male"
            elif re.search(r"\bfemale\b", joined, re.IGNORECASE):
                info["gender"] = "Female"

    # ==================================================
    # 5️⃣ AGE FROM CONTEXT (NUMBER BEFORE SEX)
    # ==================================================
    if info["age"] == "--":
        for i, line in enumerate(lines):
            if re.search(r"\bsex\b", line, re.IGNORECASE):
                for back in range(1, 4):
                    if i - back >= 0:
                        candidate = lines[i - back].strip()
                        if re.fullmatch(r"\d{1,3}", candidate):
                            age = int(candidate)
                            if 0 < age < 120:
                                info["age"] = str(age)
                                break
                break

    print("🧍 FINAL PATIENT INFO:", info)
    return info
