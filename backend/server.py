from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline_core import run_pipeline
from context_builder import ContextBuilder
from writer import agent3_generate_report
import pandas as pd
import numpy as np
import random
import pickle
import uuid
import traceback

df = pd.read_csv("dataset/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")

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

        "agent2_result": result.get("agent2_result")
    }

@app.post("/generate-report")
def generate_report(data: dict):

    print(data)

    report = agent3_generate_report(
        agent1_summary=data["agent1_summary"],
        current_flow=data["current_flow"],
        agent2_result=data["agent2_result"]
    )

    return {"report": report}