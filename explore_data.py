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