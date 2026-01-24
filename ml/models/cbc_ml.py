def predict_cbc(labs):
    """
    Predicts abnormalities from Complete Blood Count (CBC)
    """

    hemoglobin = labs.get("hemoglobin", 0)
    wbc = labs.get("wbc", 0)
    platelets = labs.get("platelets", 0)

    results = []

    # ---- Hemoglobin (Anemia Detection) ----
    if hemoglobin < 8:
        results.append("Severe Anemia Detected")
    elif 8 <= hemoglobin < 11:
        results.append("Moderate Anemia Detected")
    elif 11 <= hemoglobin < 13:
        results.append("Mild Anemia Detected")
    else:
        results.append("Normal Hemoglobin Level")

    # ---- White Blood Cells (Infection / Immunity) ----
    if wbc > 11000:
        results.append("High WBC Count – Possible Infection")
    elif wbc < 4000:
        results.append("Low WBC Count – Immunity Risk")
    else:
        results.append("Normal WBC Count")

    # ---- Platelets (Clotting Disorders) ----
    if platelets < 150000:
        results.append("Low Platelet Count (Thrombocytopenia)")
    elif platelets > 450000:
        results.append("High Platelet Count (Thrombocytosis)")
    else:
        results.append("Normal Platelet Count")

    return results
