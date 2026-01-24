import re

# ================================
# TEST KEYWORDS (CAN EXTEND)
# ================================
TEST_KEYWORDS = {
    "hemoglobin": ["hemoglobin", "haemoglobin", "hb"],
    "wbc": ["total wbc", "wbc count", "wbc"],
    "rbc": ["total rbc", "rbc count", "rbc"],
    "pcv": ["pcv", "hematocrit", "hct"],
    "mcv": ["mcv"],
    "mch": ["mch"],
    "mchc": ["mchc"],
    "rdw": ["rdw"],
    "platelets": ["platelet count", "platelets"],

    "neutrophil": ["neutrophils"],
    "lymphocyte": ["lymphocytes"],
    "monocyte": ["monocytes"],
    "eosinophil": ["eosinophils"],
    "basophil": ["basophils"],

    "hba1c": ["hba1c"],
    "fasting_glucose": ["fasting glucose", "fbs"],
    "random_glucose": ["random glucose", "rbs"],

    "creatinine": ["creatinine"],
    "urea": ["urea"],

    "total_cholesterol": ["total cholesterol"],
    "hdl": ["hdl"],
    "ldl": ["ldl"],
    "triglycerides": ["triglycerides", "tg"],

    "vitamin_d": ["vitamin d", "25 hydroxy"]
}

# ================================
# NUMBER HANDLING
# ================================
NUMBER_RE = re.compile(r"([\d,]+\.?\d*)")


def clean_number(num):
    """
    Converts:
    17,100  -> 17100
    2,06,000 -> 206000
    """
    try:
        return float(num.replace(",", ""))
    except:
        return None


# ================================
# NORMALIZE OCR LINE
# ================================
def normalize(line):
    line = line.lower()
    line = re.sub(r"\s+", " ", line)
    return line.strip()


# ================================
# CORE EXTRACTION LOGIC
# ================================
def extract_lab_values(text):
    values = {}
    lines = [normalize(l) for l in text.splitlines() if l.strip()]

    for i, line in enumerate(lines):
        for test, keywords in TEST_KEYWORDS.items():

            # Prevent overwriting correct value
            if test in values:
                continue

            if any(k in line for k in keywords):

                # Look at same line + next 2 lines
                scan_block = lines[i:i + 3]

                for blk in scan_block:
                    numbers = NUMBER_RE.findall(blk)

                    if not numbers:
                        continue

                    value = clean_number(numbers[0])
                    if value is None:
                        continue

                    # Sanity limits (medical safe)
                    if test == "platelets" and value < 1000:
                        continue  # likely ref range

                    if 0 < value < 1_000_000:
                        values[test] = value
                        break

    # ================================
    # TERMINAL DEBUG OUTPUT
    # ================================
    print("\n========== PARSED LAB VALUES ==========")
    if not values:
        print("❌ No lab values detected")
    else:
        for k, v in values.items():
            print(f"{k.upper():15} : {v}")
    print("======================================\n")

    return values


# ================================
# FINAL SANITIZER
# ================================
def sanitize_lab_values(values):
    clean = {}
    for k, v in values.items():
        try:
            clean[k] = float(v)
        except:
            pass
    return clean
