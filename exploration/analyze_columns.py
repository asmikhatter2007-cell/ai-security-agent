import pandas as pd
import numpy as np

df = pd.read_csv('dataset/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv')
df.columns = df.columns.str.strip()
df = df.replace([np.inf, -np.inf], np.nan)
print(df.columns.tolist())

columns_to_check = [
    'Total Length of Fwd Packets',
    'Flow Packets/s',
    'Fwd Packets/s',
    'Packet Length Mean',
    'Init_Win_bytes_forward',
    'Init_Win_bytes_backward',
    'Subflow Fwd Bytes'
]

print("Median values: BENIGN vs PortScan\n")
for col in columns_to_check:
    benign_median = df[df['Label'] == 'BENIGN'][col].median()
    portscan_median = df[df['Label'] == 'PortScan'][col].median()
    print(f"{col}:")
    print(f"  BENIGN median:   {benign_median}")
    print(f"  PortScan median: {portscan_median}")
    print()

short_duration = df['Flow Duration'] < 1000
no_payload = df['Total Length of Fwd Packets'] <= 5

combined_flag = short_duration & no_payload

flagged_portscan = (combined_flag & (df['Label'] == 'PortScan')).sum()
flagged_benign = (combined_flag & (df['Label'] == 'BENIGN')).sum()
total_portscan = (df['Label'] == 'PortScan').sum()
total_benign = (df['Label'] == 'BENIGN').sum()

print(f"PortScan correctly flagged: {flagged_portscan}/{total_portscan} ({100*flagged_portscan/total_portscan:.1f}%)")
print(f"BENIGN false positives: {flagged_benign}/{total_benign} ({100*flagged_benign/total_benign:.1f}%)")    