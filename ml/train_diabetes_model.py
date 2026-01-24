import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# Create models directory if not exists
os.makedirs("ml/models", exist_ok=True)

# Sample dataset (demo – replace with real data later)
data = {
    "fasting_glucose": [80, 95, 110, 140, 160, 180],
    "postprandial_glucose": [120, 130, 150, 220, 250, 300],
    "hba1c": [5.2, 5.6, 6.0, 6.8, 7.5, 9.0],
    "diabetes": [0, 0, 1, 1, 1, 1]
}

df = pd.DataFrame(data)

X = df[["fasting_glucose", "postprandial_glucose", "hba1c"]]
y = df["diabetes"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# Train SVM
svm_model = SVC(probability=True)
svm_model.fit(X_train, y_train)

# Train Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

print("SVM Accuracy:", accuracy_score(y_test, svm_model.predict(X_test)))
print("RF Accuracy:", accuracy_score(y_test, rf_model.predict(X_test)))

# Save Random Forest model
joblib.dump(rf_model, "ml/models/diabetes_model.pkl")

print("✅ Model saved at ml/models/diabetes_model.pkl")
