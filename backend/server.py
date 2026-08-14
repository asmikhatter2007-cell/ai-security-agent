from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline_core import run_pipeline
from context_builder import ContextBuilder
import pandas as pd
import numpy as np
import random
import pickle
import uuid
import traceback

files = [
    "dataset/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
    "dataset/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
    "dataset/Tuesday-WorkingHours.pcap_ISCX.csv",
    "dataset/Wednesday-workingHours.pcap_ISCX.csv",
    "dataset/Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
]

frames = [pd.read_csv(f) for f in files]

df = pd.concat(frames, ignore_index=True)

df.columns = df.columns.str.strip()
df = df.replace([np.inf, -np.inf], np.nan)
df = df[df["Init_Win_bytes_forward"] != -1]
df = df.fillna(0)
builder = ContextBuilder(df)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("Loading Random Forest model...")

with open("rf_model.pkl", "rb") as f:
    rf_model = pickle.load(f)

with open("rf_features.pkl", "rb") as f:
    rf_features = pickle.load(f)

print("Model Loaded Successfully!")


current_index = 0

class FlowData(BaseModel):
    features: dict

@app.get("/")
def home():
    return {
        "message": "AI Security Agent Backend Running"
    }

@app.get("/status")
def status():
    return {
        "model": "Loaded",
        "features": len(rf_features)
    }

@app.get("/predict")
def predict():

    global current_index

    if current_index >= len(df):
        current_index = 0

    row = df.iloc[current_index]
    current_index += 1

    X = pd.DataFrame([row[rf_features]])

    prediction = rf_model.predict(X)[0]
    probability = rf_model.predict_proba(X)[0]

    confidence = round(float(max(probability) * 100), 2)

    return {
    "id": current_index,

    "timestamp": str(row["Timestamp"]),

    "srcIp": row["Source IP"],

    "dstIp": row["Destination IP"],

    "prediction": prediction,

    "actualLabel": row["Label"],

    "confidence": confidence,

    "isBenign": prediction == "BENIGN",

    "severity": (
        "HIGH"
        if prediction != "BENIGN" and confidence >= 95
        else "MEDIUM"
        if prediction != "BENIGN"
        else "LOW"
    ),

    "verdict": None,

    "reason": None,

    "agent1": {
        "prediction": prediction,
        "confidence": confidence
    },

    "agent2": None,

    "agent3": None
}

@app.get("/next-flow")
def next_flow():

    row = df.sample(1)
    sample = row.iloc[0]

    try:
        result = run_pipeline(row, builder)

    except Exception as e:

        print("\nPIPELINE ERROR\n")
        traceback.print_exc()

        return {
            "id": str(uuid.uuid4()),
            "threat": "PIPELINE_ERROR",
            "confidence": 0,
            "severity": "LOW",
            "srcIp": sample["Source IP"],
            "dstIp": sample["Destination IP"],
            "timestamp": pd.Timestamp.now().strftime("%H:%M:%S"),
            "isBenign": True,
            "verdict": "Unavailable",
            "reason": str(e)
        }

    if result["prediction"] == "BENIGN":

        return {
            "id": str(uuid.uuid4()),
            "threat": "BENIGN",
            "confidence": round(result["confidence"], 2),
            "severity": "LOW",
            "srcIp": sample["Source IP"],
            "dstIp": sample["Destination IP"],
            "timestamp": pd.Timestamp.now().strftime("%H:%M:%S"),
            "isBenign": True,
            "verdict": None,
            "reason": None
        }

    return {

        "id": str(uuid.uuid4()),

        "threat": result["prediction"],

        "confidence": round(result["confidence"],2),

        "severity": (
            "HIGH"
            if result["confidence"] >= 90
            else "MEDIUM"
        ),

        "srcIp": sample["Source IP"],

        "dstIp": sample["Destination IP"],

        "timestamp": pd.Timestamp.now().strftime("%H:%M:%S"),

        "isBenign": False,

        "verdict": result.get("verdict"),

        "reason": result.get("reason"),

        "evidence": result.get("evidence"),

        "agent1_summary": result.get("agent1_summary"),

        "current_flow": result.get("current_flow"),

        "agent2_result": result.get("agent2_result"),

        "historical_activity": result.get("historical_activity")
    }

@app.post("/generate-report")
def generate_report(data: dict):

    verdict = data["agent2_result"]["verdict"]

    if verdict == "Supports":
        recommendation = "Escalate this incident for SOC analyst review."

    elif verdict == "Partially Supports":
        recommendation = "Review additional telemetry before escalation."

    elif verdict == "Contradicts":
        recommendation = "Revalidate the prediction using additional evidence."

    else:
        recommendation = "Collect more behavioural data before making a decision."

    history = data.get("historical_activity")

    print(history)
    print(type(history))

     

    report_data = {
        "classification": data["agent1_summary"]["prediction"],
        "confidence": data["agent1_summary"]["confidence"],

        "source": data["current_flow"]["Source IP"],
        "destination": data["current_flow"]["Destination IP"],

        "verdict": data["agent2_result"]["verdict"],
        "reason": data["agent2_result"]["reason"],
        "evidence": data["agent2_result"]["evidence"],
        "historical_activity":history,

        
        "recommendation": recommendation
    }


    if isinstance(history, dict):
        print("Keys:", history.keys())

    print("==============================\n")

    if history is not None:

        history_data = history.get("data", {})

        if history_data:
            ip = list(history_data.keys())[0]

            ip_history = history_data[ip]

            report_data["historical_activity"] = {
                "source_ip": ip,
                "first_seen": ip_history["first_seen"],
                "last_seen": ip_history["last_seen"],
                "validated_incidents": ip_history["validated_incidents"],
                "threat_counts": ip_history["threat_counts"]
            }

    report = f"""
Executive Summary:
This incident has been classified as {report_data['classification']} 
with a confidence of {report_data['confidence']}%.

Agent 2 Verdict:
{report_data['verdict']}

Reason:
{report_data['reason']}


Evidence:

"""

    for item in report_data["evidence"]:
        report += f" {item}\n"


    if report_data.get("historical_activity"):

        history = report_data["historical_activity"]

        report += f"""

Historical Activity:

Source IP: {history.get('source_ip')}
First Seen: {history.get('first_seen')}
Last Seen: {history.get('last_seen')}
Validated Incidents: {history.get('validated_incidents')}
"""

    report += "\nThreat Distribution:\n"

    for threat, count in history["threat_counts"].items():
        report += f"• {threat}: {count}\n"


    report += f"""

Recommendation:

{report_data['recommendation']}
"""


    return {
        "report": report
    }