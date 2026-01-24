import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "Anemia_processed.csv")
MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "anemia_model.pkl")

# Load dataset
df = pd.read_csv(DATASET_PATH)

# 🔹 Clean column names (VERY IMPORTANT)
df.columns = df.columns.str.strip()

# Rename useful columns
df.rename(columns={
    "Sex": "Gender",
    "HGB": "Hemoglobin"
}, inplace=True)

# Drop rows with missing values
df = df.dropna(subset=["Hemoglobin", "Gender"])

# Encode gender
df["Gender"] = df["Gender"].map({"M": 1, "F": 0})

# 🔹 Create Anemia label using medical rule
def anemia_label(row):
    if row["Gender"] == 1:  # Male
        return 1 if row["Hemoglobin"] < 13 else 0
    else:  # Female
        return 1 if row["Hemoglobin"] < 12 else 0

df["Anemia"] = df.apply(anemia_label, axis=1)

# Features & target
X = df[["Hemoglobin"]]
y = df["Anemia"]

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

print("✅ Anemia ML model trained and saved successfully")
