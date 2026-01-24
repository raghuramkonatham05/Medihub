# ml/report_classifier.py

def detect_report_type(lab_values):
    """
    Detects medical report categories based on extracted lab values.
    Designed to work with OCR-based noisy inputs.
    """

    report_types = []

    if not lab_values:
        return ["Unknown"]

    # ==================================================
    # CBC (Complete Blood Count)
    # ==================================================
    cbc_markers = [
        "hemoglobin",
        "rbc_count",
        "wbc_count",
        "platelet_count",
        "pcv",
        "mcv",
        "mch",
        "mchc",
        "rdw"
    ]
    if any(k in lab_values for k in cbc_markers):
        report_types.append("CBC")

    # ==================================================
    # DIABETES
    # ==================================================
    if (
        "hba1c" in lab_values
        or "fasting_glucose" in lab_values
        or "random_glucose" in lab_values
    ):
        report_types.append("Diabetes")

    # ==================================================
    # KIDNEY
    # ==================================================
    kidney_markers = ["creatinine", "urea", "egfr"]
    if any(k in lab_values for k in kidney_markers):
        report_types.append("Kidney")

    # ==================================================
    # LIPID PROFILE / CARDIAC RISK
    # ==================================================
    lipid_markers = [
        "total_cholesterol",
        "ldl",
        "hdl",
        "triglycerides"
    ]
    if any(k in lab_values for k in lipid_markers):
        report_types.append("Lipid")

        # Cardiac risk if LDL or very high cholesterol
        if (
            lab_values.get("ldl", 0) >= 130
            or lab_values.get("total_cholesterol", 0) >= 200
        ):
            report_types.append("Cardiac")

    # ==================================================
    # VITAMINS
    # ==================================================
    if "vitamin_d" in lab_values:
        report_types.append("Vitamins")

    # ==================================================
    # INFECTION (heuristic)
    # ==================================================
    if (
        lab_values.get("wbc_count", 0) > 11000
        or lab_values.get("neutrophils", 0) > 75
        or lab_values.get("crp", 0) > 5
    ):
        report_types.append("Infection")

    # ==================================================
    # REMOVE DUPLICATES, KEEP ORDER
    # ==================================================
    seen = set()
    final_types = []
    for r in report_types:
        if r not in seen:
            final_types.append(r)
            seen.add(r)

    return final_types
