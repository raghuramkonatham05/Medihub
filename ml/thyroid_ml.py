import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("ml", "models", "thyroid_model.pkl")
model = joblib.load(MODEL_PATH)

def predict_thyroid_ml(lab):
    """
    Thyroid prediction using trained ML model.
    Proxy-based due to dataset limitations.
    """

    # Default proxy values (used when lab report lacks data)
    age = lab.get("age", 40)        # average adult
    gender = lab.get("gender", 0)   # 0 = female, 1 = male
    smoking = lab.get("smoking", 0) # assume non-smoker

    X = np.array([[age, gender, smoking]])
    pred = model.predict(X)[0]

    if pred == 1:
        return "Possible Thyroid Abnormality (ML-based)"
    else:
        return "Normal Thyroid Function (ML-based)"
