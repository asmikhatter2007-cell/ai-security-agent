import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pickle

# ============================================================
# LOAD AND CLEAN DATA
# ============================================================

print("Loading dataset...")
import glob

files = glob.glob("backend/dataset/*.csv")
  # or "dataset/*.csv" if in folder

dfs = []

for file in files:
    print("Loading:", file)
    temp = pd.read_csv(file, low_memory=False)
    temp.columns = temp.columns.str.strip()
    dfs.append(temp)

df = pd.concat(dfs, ignore_index=True)

print("Total rows:", len(df))
print(df["Label"].value_counts())
df.columns = df.columns.str.strip()
df["Label"] = df["Label"].astype(str).str.strip()
df = df.replace([np.inf, -np.inf], np.nan)
df = df[df['Init_Win_bytes_forward'] != -1]
df = df.dropna(subset=['Flow Duration', 
                        'Total Length of Fwd Packets',
                        'Init_Win_bytes_forward',
                        'Destination Port' ,
                        'Label'])

print(f"Rows after cleaning: {len(df)}")
print(f"Labels: {df['Label'].value_counts().to_dict()}")

# ============================================================
# FEATURE SELECTION
# Using our 3 validated research-confirmed signals
# plus additional features for RF to discover patterns
# ============================================================

FEATURES = [
    'Flow Duration',                    # Signal 1 — validated
    'Total Length of Fwd Packets',      # Signal 2 — validated  
    'Init_Win_bytes_forward',           # Signal 3 — validated
    'Destination Port',                 # For entropy patterns
    'Total Fwd Packets',               # Flow structure
    'Total Backward Packets',          # Response pattern
    'Fwd Packet Length Mean',          # Packet size
    'Flow Packets/s',                  # Speed metric
    'SYN Flag Count',                  # TCP handshake
    'ACK Flag Count',                  # TCP acknowledgment
    'RST Flag Count',                  # Connection resets
    'Fwd Header Length',               # Header size
]

X = df[FEATURES]
y = df['Label']

print(f"\nFeatures: {FEATURES}")
print(f"Target classes: {y.unique()}")

# ============================================================
# TRAIN/TEST SPLIT
# 80% training, 20% testing
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y  # ensures both classes represented in train and test
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# ============================================================
# TRAIN RANDOM FOREST
# ============================================================

print("\nTraining Random Forest...")
rf = RandomForestClassifier(
    n_estimators=100,    # 100 decision trees
    random_state=42,
    n_jobs=-1            # use all CPU cores
)
rf.fit(X_train, y_train)
print("Training complete.")

# ============================================================
# EVALUATE
# ============================================================

print("\n" + "="*50)
print("EVALUATION RESULTS")
print("="*50)

y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ============================================================
# FEATURE IMPORTANCE
# This will confirm our validated signals appear at the top
# ============================================================

print("\n" + "="*50)
print("FEATURE IMPORTANCE (confirms our validated signals)")
print("="*50)

importances = list(zip(FEATURES, rf.feature_importances_))
importances.sort(key=lambda x: x[1], reverse=True)

for feature, importance in importances:
    bar = "█" * int(importance * 50)
    print(f"{feature:<35} {importance:.4f} {bar}")

# ============================================================
# SAVE MODEL
# ============================================================

with open('rf_model.pkl', 'wb') as f:
    pickle.dump(rf, f)

with open('rf_features.pkl', 'wb') as f:
    pickle.dump(FEATURES, f)

print("\nModel saved to rf_model.pkl")
print("Features saved to rf_features.pkl")
print("\nAgent 1 (Random Forest) is ready.")