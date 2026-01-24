import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("ml", "models", "anemia_model.pkl")
model = joblib.load(MODEL_PATH)

def predict_anemia_ml(lab_values):
    """
    Predict anemia using ML model
    Feature used: hemoglobin
    """

    if "hemoglobin" not in lab_values:
        return "Insufficient data for Anemia prediction"

    try:
        hb = float(lab_values["hemoglobin"])
    except ValueError:
        return "Invalid hemoglobin value"

    X = np.array([[hb]])
    prob = model.predict_proba(X)[0][1]

    if prob >= 0.7:
        return f"Severe Anemia (Probability: {prob:.2f})"
    elif prob >= 0.4:
        return f"Moderate Anemia (Probability: {prob:.2f})"
    else:
        return f"Normal (Probability: {1 - prob:.2f})"
