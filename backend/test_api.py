import pandas as pd
import requests
import pickle

# Load the feature names
with open("rf_features.pkl", "rb") as f:
    rf_features = pickle.load(f)

# Load one row from your dataset
df = pd.read_csv("dataset/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")

df.columns = df.columns.str.strip()

# Take the first row
sample = df.iloc[0]

# Build payload using only model features
payload = {
    "features": {
        feature: float(sample[feature]) if pd.notna(sample[feature]) else 0
        for feature in rf_features
    }
}

response = requests.post(
    "http://127.0.0.1:8000/predict",
    json=payload
)

print(response.json())