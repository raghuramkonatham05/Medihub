import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "thyroid.csv")
MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "thyroid_model.pkl")

# Load dataset
df = pd.read_csv(DATASET_PATH)

# Select features and target
features = ["Age", "Gender", "Smoking"]
target = "Thyroid Function"

df = df[features + [target]].dropna()

# Encode categorical columns
encoder = LabelEncoder()
df["Gender"] = encoder.fit_transform(df["Gender"])
df["Smoking"] = encoder.fit_transform(df["Smoking"])
df[target] = encoder.fit_transform(df[target])

X = df[features]
y = df[target]

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

print("✅ Thyroid ML model trained successfully")
