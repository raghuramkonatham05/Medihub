# ocr/lab_parser.py

import re

# ==================================================
# TEST DEFINITIONS
# ==================================================
TESTS = {
    "hemoglobin": ["hemoglobin", "haemoglobin", "hb", "h b", "h.b"],
    "rbc": ["rbc count", "rbc"],
    "pcv": ["pcv", "hematocrit", "hct"],
    "mcv": ["mcv"],
    "mch": ["mch"],
    "mchc": ["mchc"],
    "wbc": ["total wbc count", "total wbc", "wbc"],
    "platelets": ["platelet count", "platelets", "platelet"],
    "lymphocyte": ["lymphocytes", "lymphocyte"],
    "eosinophil": ["eosinophils", "eosinophil"],
    "monocyte": ["monocytes", "monocyte"],
    "neutrophils": ["polymorphs", "neutrophils"],
}

# Match decimal OR integer (preserves decimals correctly)
NUMBER_RE = re.compile(r"\d+\.\d+|\d+,?\d*")


# ==================================================
# NORMALIZATION (FIXED — DOES NOT REMOVE DECIMALS)
# ==================================================
def normalize(line: str) -> str:
    line = line.lower()
    line = re.sub(r":", "", line)      # remove only colon
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def to_float(val: str):
    try:
        return float(val.replace(",", ""))
    except:
        return None


# ==================================================
# CORE EXTRACTION
# Works for:
# 1. Same-line values (PDF)
# 2. Next-line values (OCR images)
# ==================================================
def extract_lab_values(text: str) -> dict:
    values = {}
    lines = [normalize(l) for l in text.splitlines() if l.strip()]

    for i, line in enumerate(lines):
        for test, aliases in TESTS.items():

            if test in values:
                continue

            if any(alias in line for alias in aliases):

                # 1️⃣ Try extracting from same line
                nums = NUMBER_RE.findall(line)
                if nums:
                    val = to_float(nums[0])
                    if val is not None:
                        values[test] = val
                        continue

                # 2️⃣ Try next 2 lines (OCR case)
                for nxt in lines[i + 1:i + 3]:
                    nums = NUMBER_RE.findall(nxt)
                    if nums:
                        val = to_float(nums[0])
                        if val is not None:
                            values[test] = val
                            break

    # ================= DEBUG =================
    print("\n========== PARSED LAB VALUES ==========")
    for k, v in values.items():
        print(f"{k.upper():15} : {v}")
    print("======================================\n")

    return sanitize_lab_values(values)


# ==================================================
# SANITIZATION (ONLY DECIMAL CORRECTIONS)
# ==================================================
def sanitize_lab_values(values: dict) -> dict:
    clean = {}

    for test, value in values.items():

        if value is None:
            continue

        # Fix decimal shift errors from OCR only

        if test == "hemoglobin" and value > 30:
            value = value / 10

        if test == "rbc" and value > 10:
            value = value / 100

        if test == "pcv" and value > 100:
            value = value / 10

        if test in ["mcv", "mch", "mchc"] and value > 150:
            value = value / 10

        # IMPORTANT: No platelet multiplication or scaling

        clean[test] = round(value, 2)

    return clean