# ml/liver_ml.py

import os
import joblib
import pandas as pd

# =============================
# LOAD TRAINED MODEL
# =============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "liver_model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("❌ Liver ML model not found. Train it first.")

model = joblib.load(MODEL_PATH)

# =============================
# REQUIRED FEATURES (FROM DATASET)
# =============================
FEATURES = [
    "age",
    "gender",
    "tot_bilirubin",
    "direct_bilirubin",
    "tot_proteins",
    "albumin",
    "ag_ratio",
    "sgpt",
    "sgot",
    "alkphos",
]

# =============================
# PREDICTION FUNCTION
# =============================
def predict_liver_ml(lab_values: dict, patient: dict = None):
    """
    Predicts liver disease risk using lab values + patient info
    Returns human-readable result for dashboard
    """

    data = {}

    # -----------------------------
    # AGE
    # -----------------------------
    try:
        data["age"] = int(patient.get("age")) if patient else 45
    except Exception:
        data["age"] = 45

    # -----------------------------
    # GENDER
    # -----------------------------
    gender = (patient or {}).get("gender", "").lower()
    if gender == "male":
        data["gender"] = 1
    elif gender == "female":
        data["gender"] = 0
    else:
        data["gender"] = 1  # default male (safe medical bias)

    # -----------------------------
    # LAB VALUES (SAFE DEFAULTS)
    # -----------------------------
    defaults = {
        "tot_bilirubin": 1.0,
        "direct_bilirubin": 0.3,
        "tot_proteins": 6.8,
        "albumin": 3.5,
        "ag_ratio": 1.0,
        "sgpt": 40,
        "sgot": 40,
        "alkphos": 120,
    }

    for key in defaults:
        data[key] = float(lab_values.get(key, defaults[key]))

    # -----------------------------
    # CREATE DATAFRAME
    # -----------------------------
    X = pd.DataFrame([data], columns=FEATURES)

    # -----------------------------
    # PREDICT
    # -----------------------------
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]

    # -----------------------------
    # HUMAN OUTPUT
    # -----------------------------
    if prediction == 1:
        return {
            "risk": "High",
            "confidence": f"{round(probability * 100, 1)}%",
            "message": "Signs indicate possible liver disease. Clinical correlation advised."
        }
    else:
        return {
            "risk": "Normal",
            "confidence": f"{round((1 - probability) * 100, 1)}%",
            "message": "No significant liver disease patterns detected."
        }
