import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "kidney_disease.csv")
MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "kidney_model.pkl")

# Load dataset
df = pd.read_csv(DATASET_PATH)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Columns
CREATININE_COL = "sc"              # serum creatinine
TARGET_COL = "classification"

# Drop missing values
df = df.dropna(subset=[CREATININE_COL, TARGET_COL])

# 🔹 CLEAN TARGET VALUES (THIS FIXES YOUR ERROR)
df[TARGET_COL] = (
    df[TARGET_COL]
    .astype(str)
    .str.strip()
    .str.lower()
)

# Map target to numeric
df[TARGET_COL] = df[TARGET_COL].map({
    "ckd": 1,
    "notckd": 0
})

# Drop rows that couldn't be mapped
df = df.dropna(subset=[TARGET_COL])

df[TARGET_COL] = df[TARGET_COL].astype(int)

# Features & target
X = df[[CREATININE_COL]]
y = df[TARGET_COL]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save model
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("✅ Kidney ML model trained and saved successfully")
