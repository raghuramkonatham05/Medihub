# ocr/lab_explanations.py

EXPLANATIONS = {
    "hemoglobin": {
        "low": "Low hemoglobin may indicate anemia, which can cause fatigue and weakness.",
        "normal": "Hemoglobin level is normal and indicates healthy oxygen transport.",
        "high": "High hemoglobin may be linked to dehydration or other conditions."
    },

    "hba1c": {
        "low": "HbA1c is within a healthy range.",
        "normal": "Blood sugar levels are well controlled.",
        "high": "High HbA1c suggests poor blood sugar control and risk of diabetes."
    },

    "fasting_glucose": {
        "low": "Low blood sugar may cause dizziness or weakness.",
        "normal": "Fasting glucose is within a healthy range.",
        "high": "High fasting glucose may indicate diabetes risk."
    },

    "total_cholesterol": {
        "normal": "Cholesterol level is within a healthy range.",
        "high": "High cholesterol increases the risk of heart disease."
    },

    "vitamin_d": {
        "low": "Vitamin D deficiency may cause bone weakness and low immunity.",
        "normal": "Vitamin D level is sufficient.",
        "high": "Very high vitamin D levels can be harmful."
    }
}


def explain(test, status):
    return EXPLANATIONS.get(test, {}).get(
        status,
        "No explanation available."
    )
