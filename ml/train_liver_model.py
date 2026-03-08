import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "liver.csv")
MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "liver_model.pkl")

# ==============================
# LOAD DATASET
# ==============================
df = pd.read_csv(DATASET_PATH)

# Normalize column names
df.columns = df.columns.str.strip().str.lower()
print("🧾 Dataset columns:", df.columns.tolist())

# ==============================
# CLEAN GENDER COLUMN (CRITICAL FIX)
# ==============================
if "gender" not in df.columns:
    raise ValueError("❌ Gender column not found")

df["gender"] = (
    df["gender"]
    .astype(str)
    .str.strip()
    .str.lower()
)

df["gender"] = df["gender"].replace({
    "male": 1,
    "female": 0,
    "m": 1,
    "f": 0
})

# ==============================
# TARGET COLUMN
# ==============================
if "is_patient" not in df.columns:
    raise ValueError("❌ Target column (is_patient) not found")

df["is_patient"] = df["is_patient"].replace({1: 1, 2: 0})

# ==============================
# REMOVE ONLY INVALID ROWS
# ==============================
df = df.dropna(subset=["gender", "is_patient"])

print("✅ Rows after cleaning:", len(df))

if len(df) < 20:
    raise ValueError("❌ Dataset too small after cleaning")

# ==============================
# FEATURES / TARGET
# ==============================
X = df.drop("is_patient", axis=1)
y = df["is_patient"]

# ==============================
# TRAIN MODEL
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# ==============================
# SAVE MODEL
# ==============================
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("✅ Liver Disease ML model trained successfully")
