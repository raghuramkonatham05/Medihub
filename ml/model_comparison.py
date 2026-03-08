# ml/model_comparison.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    roc_curve,
    auc
)

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier


# ==========================================================
# 1️⃣ CHANGE DATASET NAME HERE ONLY
# ==========================================================

DATASET_NAME = "kidney_disease.csv"
# Examples:
# "Anemia_processed.csv"
# "diabetes.csv"
# "kidney_disease.csv"
# "liver.csv"
# "thyroid.csv"

# ==========================================================
# 2️⃣ LOAD DATASET
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataset_path = os.path.join(BASE_DIR, "datasets", DATASET_NAME)

data = pd.read_csv(dataset_path)

print("\nDataset Shape:", data.shape)

# ==========================================================
# 3️⃣ SEPARATE FEATURES & TARGET
# ==========================================================

target_column = data.columns[-1]

X = data.drop(target_column, axis=1)
y = data[target_column]

# Encode target automatically
le = LabelEncoder()
y = le.fit_transform(y)

num_classes = len(np.unique(y))
print("Number of Classes:", num_classes)

# ==========================================================
# 4️⃣ HANDLE NUMERIC & CATEGORICAL FEATURES
# ==========================================================

numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
categorical_features = X.select_dtypes(include=["object"]).columns

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features)
])

# ==========================================================
# 5️⃣ TRAIN TEST SPLIT (Safe Split)
# ==========================================================

try:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y if num_classes < 50 else None
    )
except:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

# ==========================================================
# 6️⃣ DEFINE MODELS (TUNED & STABLE)
# ==========================================================

models = {
    "Logistic Regression": Pipeline([
        ("preprocess", preprocessor),
        ("model", LogisticRegression(max_iter=5000))
    ]),
    "SVM": Pipeline([
        ("preprocess", preprocessor),
        ("model", SVC(probability=True, kernel="rbf"))
    ]),
    "Random Forest": Pipeline([
        ("preprocess", preprocessor),
        ("model", RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            random_state=42
        ))
    ])
}

results = {}
cv_scores = {}
conf_matrices = {}

print("\n🔎 MODEL EVALUATION RESULTS:\n")

# ==========================================================
# 7️⃣ TRAIN + CROSS VALIDATION + EVALUATE
# ==========================================================

for name, model in models.items():

    # Cross Validation (5-Fold)
    cv = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
    cv_scores[name] = cv.mean()

    # Train
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)

    results[name] = acc
    conf_matrices[name] = confusion_matrix(y_test, y_pred)

    print(f"{name}")
    print(f"Cross-Val Accuracy: {cv.mean():.4f}")
    print(f"Test Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))
    print("-" * 50)

# ==========================================================
# 8️⃣ BEST MODEL SELECTION
# ==========================================================

best_model = max(results, key=results.get)
best_model_obj = models[best_model]

print("\n🏆 BEST MODEL:", best_model)
print("Best Test Accuracy:", results[best_model])

# ==========================================================
# 9️⃣ ACCURACY GRAPH
# ==========================================================

plt.figure(figsize=(8, 5))
plt.bar(results.keys(), results.values())
plt.xlabel("Models")
plt.ylabel("Test Accuracy")
plt.title(f"Model Comparison ({DATASET_NAME})")
plt.xticks(rotation=25)
plt.tight_layout()
plt.show()

# ==========================================================
# 🔟 CONFUSION MATRIX
# ==========================================================

plt.figure(figsize=(6, 5))
ConfusionMatrixDisplay(conf_matrices[best_model]).plot()
plt.title(f"Confusion Matrix - {best_model}")
plt.tight_layout()
plt.show()

# ==========================================================
# ROC CURVE (Binary Only - Fully Safe)
# ==========================================================

if num_classes == 2:

    try:
        y_prob = best_model_obj.predict_proba(X_test)[:, 1]

        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)

        print("\nAUC Score:", roc_auc)

        plt.figure(figsize=(6, 5))
        plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.4f}")
        plt.plot([0, 1], [0, 1], linestyle="--")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title(f"ROC Curve - {best_model} ({DATASET_NAME})")
        plt.legend()
        plt.tight_layout()

        # ✅ Dynamic filename (VERY IMPORTANT)
        roc_filename = DATASET_NAME.replace(".csv", "_roc.png")
        plt.savefig(roc_filename, dpi=300)
        plt.close()

        print(f"ROC Curve saved as: {roc_filename}")

    except Exception as e:
        print("\nROC generation skipped due to:", e)

else:
    print("\nROC skipped (Multi-class dataset)")
