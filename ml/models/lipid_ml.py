def predict_lipid(lab_values):
    findings = []

    cholesterol = lab_values.get("total_cholesterol")
    ldl = lab_values.get("ldl")
    hdl = lab_values.get("hdl")
    triglycerides = lab_values.get("triglycerides")

    if cholesterol and cholesterol > 200:
        findings.append("High Total Cholesterol")

    if ldl and ldl > 130:
        findings.append("High LDL – Cardiac Risk")

    if hdl and hdl < 40:
        findings.append("Low HDL – Poor Heart Protection")

    if triglycerides and triglycerides > 150:
        findings.append("High Triglycerides")

    if not findings:
        findings.append("Lipid profile is within normal range")

    return findings
