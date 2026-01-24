def predict_cbc(lab_values):
    findings = []

    hb = lab_values.get("hemoglobin")
    wbc = lab_values.get("wbc")
    platelets = lab_values.get("platelets")

    if hb is not None and hb < 11:
        findings.append("Severe Anemia Detected")

    if wbc is not None and (wbc < 4000 or wbc > 11000):
        findings.append("Possible Infection / Inflammation")

    if platelets is not None and platelets < 150000:
        findings.append("Low Platelet Count (Thrombocytopenia)")

    if not findings:
        findings.append("CBC parameters are within normal range")

    return findings
