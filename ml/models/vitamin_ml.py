def predict_vitamins(labs):
    vit_d = labs.get("vitamin_d", 50)
    b12 = labs.get("vitamin_b12", 500)

    results = []
    if vit_d < 20:
        results.append("Vitamin D Deficiency")
    if b12 < 200:
        results.append("Vitamin B12 Deficiency")

    return results if results else ["No Vitamin Deficiency"]
