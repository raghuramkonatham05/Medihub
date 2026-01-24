# ocr/lab_flags.py

REFERENCE_RANGES = {
    "hemoglobin": (11.0, 18.0),
    "wbc": (4000, 11000),
    "neutrophil": (40, 65),
    "lymphocyte": (30, 60),
    "eosinophil": (1, 6),
    "monocyte": (2, 10),
    "rbc": (4.5, 6.0),
    "pcv": (42, 52),
    "mcv": (76, 96),
    "mch": (27, 32),
    "mchc": (32, 36),
    "platelets": (150000, 450000),  # absolute count
}

def flag_lab_values(lab_values):
    flags = {}

    for test, value in lab_values.items():
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
            "value": value,
            "status": status,
            "color": color,
            "range": f"{low} - {high}"
        }

    # 🔎 DEBUG (keep this)
    print("\n========== FLAGS GENERATED ==========")
    for k, v in flags.items():
        print(k, v)
    print("====================================\n")

    return flags
