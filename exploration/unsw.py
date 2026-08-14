import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# ============================================================
# LOAD DATA
# ============================================================

print("Loading dataset...")

df = pd.read_csv("UNSW_NB15_training-set.csv", low_memory=False)

# If you also have test file, uncomment:
# test_df = pd.read_csv("UNSW_NB15_testing-set.csv")
# df = pd.concat([df, test_df], ignore_index=True)


print("Columns:", df.columns)

# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = df.columns.str.strip()

# ============================================================
# LABEL PREPARATION
# ============================================================

# UNSW: 0 = BENIGN, 1 = ATTACK
df["Label"] = df["label"].map({0: "BENIGN", 1: "ATTACK"})

print("\nLabel distribution:")
print(df["Label"].value_counts())

# ============================================================
# FEATURE SELECTION
# (Numeric features only — no id, no categorical yet)
# ============================================================

FEATURES = [
    "dur",
    "spkts",
    "dpkts",
    "sbytes",
    "dbytes",
    "rate",
    "sttl",
    "dttl",
    "sload",
    "dload",
    "sloss",
    "dloss",
    "smean",
    "dmean"
]

# ============================================================
# HANDLE MISSING / INF VALUES
# ============================================================

df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=FEATURES + ["Label"])

# ============================================================
# SPLIT DATA
# ============================================================

X = df[FEATURES]
y = df["Label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# ============================================================
# TRAIN MODEL
# ============================================================

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training complete.")

# ============================================================
# EVALUATION
# ============================================================

print("\n================ RESULTS ================\n")

y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ============================================================
# FEATURE IMPORTANCE
# ============================================================

print("\n================ FEATURE IMPORTANCE ================\n")

importances = list(zip(FEATURES, model.feature_importances_))
importances.sort(key=lambda x: x[1], reverse=True)

for feature, importance in importances:
    bar = "█" * int(importance * 40)
    print(f"{feature:<15} {importance:.4f} {bar}")