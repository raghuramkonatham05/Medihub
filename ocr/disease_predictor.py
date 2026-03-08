def predict_diseases(lab_values):
    diseases = []

    hb = lab_values.get("hemoglobin")
    mcv = lab_values.get("mcv")
    hba1c = lab_values.get("hba1c")
    creatinine = lab_values.get("creatinine")

    # ---------------- ANEMIA ----------------
    if hb is not None:
        if hb < 7:
            severity = "Severe"
        elif hb < 11:
            severity = "Moderate"
        else:
            severity = None

        if severity:
            diseases.append({
                "name": "Anemia",
                "severity": severity,
                "reason": f"Hemoglobin is low ({hb} g/dL)"
            })

            if mcv is not None and mcv < 76:
                diseases.append({
                    "name": "Iron Deficiency Anemia",
                    "severity": severity,
                    "reason": "Low Hemoglobin + Low MCV"
                })

    # ---------------- DIABETES ----------------
    if hba1c is not None and hba1c >= 6.5:
        diseases.append({
            "name": "Diabetes Mellitus",
            "severity": "High",
            "reason": f"HbA1c is high ({hba1c}%)"
        })

    # ---------------- KIDNEY ISSUE ----------------
    if creatinine is not None and creatinine > 1.3:
        diseases.append({
            "name": "Possible Kidney Dysfunction",
            "severity": "Warning",
            "reason": f"Creatinine elevated ({creatinine} mg/dL)"
        })

    return diseases
