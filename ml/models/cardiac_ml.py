def predict_cardiac(labs):
    troponin = labs.get("troponin", 0)
    ckmb = labs.get("ckmb", 0)

    if troponin > 0.04 or ckmb > 5:
        return "⚠ Possible Cardiac Injury"
    return "No Acute Cardiac Risk"
