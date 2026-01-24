def predict_liver(lab_values):
    findings = []

    sgot = lab_values.get("sgot")
    sgpt = lab_values.get("sgpt")
    bilirubin = lab_values.get("bilirubin")

    if sgot and sgot > 40:
        findings.append("Elevated SGOT – Possible Liver Injury")

    if sgpt and sgpt > 40:
        findings.append("Elevated SGPT – Liver Inflammation Detected")

    if bilirubin and bilirubin > 1.2:
        findings.append("High Bilirubin – Possible Liver Dysfunction")

    if not findings:
        findings.append("Liver parameters are within normal range")

    return findings
