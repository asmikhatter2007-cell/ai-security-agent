import pandas as pd
import numpy as np

df = pd.read_csv('Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv')
df.columns = df.columns.str.strip()
df = df.replace([np.inf, -np.inf], np.nan)

print("Labels in this file:")
print(df['Label'].value_counts())

print("\n--- Flow Duration Comparison ---")
for label in df['Label'].unique():
    median_duration = df[df['Label'] == label]['Flow Duration'].median()
    print(f"{label}: median duration = {median_duration}")