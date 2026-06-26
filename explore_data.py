import pandas as pd

df = pd.read_csv('Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv')

print("Columns in this dataset:")
print(df.columns.tolist())

print(f"\nTotal rows: {len(df)}")

print("\nLabel distribution:")
print(df.columns[-1])  # show us the actual last column name first
print(df[df.columns[-1]].value_counts())

print("\nFirst 5 rows:")
print(df.head())

import pandas as pd

df = pd.read_csv("Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv", low_memory=False)

# IMPORTANT: strip spaces FIRST
df.columns = df.columns.str.strip()


print(df["Timestamp"].head(10))
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
print(df["Timestamp"].isna().sum())

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    format="%d/%m/%Y %H:%M",
    errors="coerce"
)

print(df["Timestamp"].dtype)
print(df["Timestamp"].head())