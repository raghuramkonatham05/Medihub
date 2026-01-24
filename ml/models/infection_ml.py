def predict_infection(labs):
    wbc = labs.get("wbc", 0)
    neutrophils = labs.get("neutrophils", 0)
    crp = labs.get("crp", 0)

    if wbc > 11000 and neutrophils > 70:
        return "High Risk of Bacterial Infection"
    elif crp > 10:
        return "Inflammation Detected"
    else:
        return "No Infection Detected"
