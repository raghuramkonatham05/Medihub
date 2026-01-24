def recommend_tests(report_types, lab_values):
    recommendations = []

    if "CBC" in report_types and lab_values.get("hemoglobin", 99) < 12:
        recommendations.append("Complete Blood Count (Follow-up)")

    if "Diabetes" in report_types:
        if lab_values.get("hba1c", 0) >= 6.5:
            recommendations.append("HbA1c")
        if lab_values.get("fasting_glucose", 0) > 126:
            recommendations.append("Fasting Blood Glucose")
        if lab_values.get("postprandial_glucose", 0) > 200:
            recommendations.append("Postprandial Blood Glucose")

    if "Kidney" in report_types and lab_values.get("creatinine", 0) > 1.5:
        recommendations += ["Serum Creatinine", "Urine Albumin", "Urea"]

    if "Thyroid" in report_types:
        recommendations += ["TSH", "T3", "T4"]

    return list(set(recommendations))
