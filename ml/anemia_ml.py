import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("ml", "models", "anemia_model.pkl")
model = joblib.load(MODEL_PATH)


def predict_anemia_ml(lab_values):
    """
    Predict anemia using ML model
    Feature used: hemoglobin (robust key handling)
    """

    hb = None

    # 🔑 Normalize keys
    for key, value in lab_values.items():
        k = key.lower().replace(".", "").replace(" ", "")
        if k in ["hb", "hemoglobin"]:
            try:
                hb = float(value)
                break
            except ValueError:
                return "Invalid hemoglobin value"

    # ❌ No hemoglobin found
    if hb is None:
        return "Insufficient data for Anemia prediction"

    # ML prediction
    X = np.array([[hb]])
    prob = model.predict_proba(X)[0][1]

    if prob >= 0.7:
        return f"Severe Anemia (Probability: {prob:.2f})"
    elif prob >= 0.4:
        return f"Moderate Anemia (Probability: {prob:.2f})"
    else:
        return f"Normal (Probability: {1 - prob:.2f})"
