import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("ml", "models", "kidney_model.pkl")
model = joblib.load(MODEL_PATH)

def predict_kidney_ml(lab):
    if "sc" not in lab and "creatinine" not in lab:
        return "Insufficient data for Kidney prediction"

    creatinine = lab.get("creatinine", lab.get("sc"))

    X = np.array([[creatinine]])
    prob = model.predict_proba(X)[0][1]

    if prob > 0.7:
        return f"High Kidney Disease Risk (Probability: {prob:.2f})"
    elif prob > 0.4:
        return f"Moderate Kidney Disease Risk (Probability: {prob:.2f})"
    else:
        return f"Low Kidney Disease Risk (Probability: {prob:.2f})"
