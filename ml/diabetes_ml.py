import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("ml", "models", "diabetes_model.pkl")
model = joblib.load(MODEL_PATH)


def predict_diabetes_ml(lab):
    """
    Predict diabetes risk using ML model
    """

    # Ensure at least one relevant value exists
    if not any(k in lab for k in ["fasting_glucose", "postprandial_glucose", "hba1c"]):
        return "Insufficient data for Diabetes prediction"

    X = np.array([[
        lab.get("fasting_glucose", 0),
        lab.get("postprandial_glucose", 0),
        lab.get("hba1c", 0)
    ]])

    probability = model.predict_proba(X)[0][1]

    if probability < 0.3:
        return f"Low Risk (Probability: {probability:.2f})"
    elif probability < 0.6:
        return f"Moderate Risk (Probability: {probability:.2f})"
    else:
        return f"High Risk (Probability: {probability:.2f})"
