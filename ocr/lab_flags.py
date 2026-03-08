# ocr/lab_flags.py

REFERENCE_RANGES = {
    "hemoglobin": (11.0, 18.0),
    "rbc": (4.5, 6.0),
    "pcv": (42, 52),
    "mcv": (76, 96),
    "mch": (27, 32),
    "mchc": (32, 36),
    "wbc": (4000, 11000),
    "neutrophils": (40, 65),
    "lymphocyte": (30, 60),
    "eosinophil": (1, 6),
    "monocyte": (2, 10),
    "platelets": (1.5, 4.5),   # ✅ In lakhs
}


# ==================================================
# UNIT NORMALIZATION (ONLY DECIMAL FIXES)
# ==================================================
def normalize_units(test, value):

    # Hemoglobin decimal-loss fix (68 → 6.8)
    if test == "hemoglobin" and value > 30:
        return value / 10

    # RBC decimal loss (311 → 3.11)
    if test == "rbc" and value > 10:
        return value / 100

    # PCV decimal loss (229 → 22.9)
    if test == "pcv" and value > 100:
        return value / 10

    # Indices decimal loss (736 → 73.6 etc)
    if test in ["mcv", "mch", "mchc"] and value > 150:
        return value / 10

    # ❌ IMPORTANT: NO platelet multiplication

    return value


# ==================================================
# FLAG GENERATION
# ==================================================
def flag_lab_values(lab_values):
    flags = {}

    for test, raw_value in lab_values.items():

        value = normalize_units(test, raw_value)

        ref = REFERENCE_RANGES.get(test)
        if not ref:
            continue

        low, high = ref

        if value < low:
            status = "low"
            color = "low"
        elif value > high:
            status = "high"
            color = "high"
        else:
            status = "normal"
            color = "normal"

        flags[test] = {
            "value": round(value, 2),
            "status": status,
            "color": color,
            "range": f"{low} - {high}",
        }

    print("\n========== FLAGS GENERATED ==========")
    for k, v in flags.items():
        print(k, v)
    print("====================================\n")

    return flags