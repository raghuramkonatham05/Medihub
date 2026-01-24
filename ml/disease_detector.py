def detect_possible_diseases(lab_values):
    diseases = []

    # Diabetes detection
    if "fasting_glucose" in lab_values or "hba1c" in lab_values:
        diseases.append("diabetes")

    # Anemia detection
    if "hemoglobin" in lab_values:
        diseases.append("anemia")

    # Thyroid detection
    if "tsh" in lab_values or "t3" in lab_values or "t4" in lab_values:
        diseases.append("thyroid")

    # Kidney detection
    if "creatinine" in lab_values:
        diseases.append("kidney")

    return diseases
