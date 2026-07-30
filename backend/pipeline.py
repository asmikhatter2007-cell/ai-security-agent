from context_builder import ContextBuilder
from writer import agent3_generate_report
from historical_activity import HistoricalActivity
import pandas as pd
import numpy as np
import pickle
import requests
import json

# ============================================================
# LOAD MODEL
# ============================================================

print("Loading Agent 1...")

with open("rf_model.pkl", "rb") as f:
    rf_model = pickle.load(f)

with open("rf_features.pkl", "rb") as f:
    rf_features = pickle.load(f)


print("Agent 1 is ready")

history=HistoricalActivity()


# ============================================================
# CONTEXT FORMATTER (SOC BRIEF)
# ============================================================

def build_context_brief(context):
    """
    Lightweight SOC-style summary for LLM reasoning.
    No interpretation, only structured summarization.
    """

    brief = []

    agent1 = context["agent1_summary"]
    flow = context["current_flow"]
    behaviour = context.get("behaviour_summary", {})

    brief.append(f"AGENT 1: {agent1['prediction']} ({agent1['confidence']}%)\n")

    brief.append("FLOW SNAPSHOT:")
    for k in ["Flow Duration", "Total Fwd Packets", "Total Backward Packets",
              "Flow Bytes/s", "Flow Packets/s"]:
        if k in flow:
            brief.append(f"- {k}: {flow[k]}")

    brief.append("\nBEHAVIOURAL SIGNALS:")
    for attack_type, stats in behaviour.items():
        if attack_type == "history_scope":
            continue
        brief.append(f"\n{attack_type}:")
        for k, v in stats.items():
            brief.append(f"- {k}: {v}")

    return "\n".join(brief)


# ============================================================
# AGENT 2
# ============================================================

def agent2_analyze(structured_data, context_brief):

    prompt = f"""
Prediction:
{structured_data["agent1_summary"]["prediction"]}

Behavioural Evidence:
{json.dumps(structured_data["behaviour_summary"], indent=2)}

Task:

You are NOT acting as an intrusion detection system.

Agent 1 has already made the prediction.

Your ONLY responsibility is to check whether the behavioural observations are CONSISTENT with Agent 1's prediction.

Treat every behavioural observation as factual.

Kindly follow the behavioural priority strictly.

Behavioural Priority:

When evaluating behavioural consistency, give higher importance to the observations that are most relevant to the predicted attack.

For PortScan, prioritize:
- destination diversity
- repeated connection patterns
- timing between flows
- payload characteristics

For DDoS, DoS Hulk, DoS GoldenEye, DoS Slowloris, DoS Slowhttptest, prioritize:
- request frequency
- destination concentration
- payload characteristics
- most targeted port

For Brute Force,SSH-Patator,FTP-Patator, prioritize:
- repeated authentication attempts
- repeated targeting behaviour
- timing between attempts

These are priorities for reasoning only.
They are NOT decision rules.
Do NOT invent thresholds or additional evidence.

Do NOT determine whether an attack occurred.

Do NOT decide whether there is enough evidence.

Do NOT estimate confidence.

Only use behavioural evidence explicitly present in the provided context. Do not infer whether a metric is high, low, abnormal, or typical unless the context explicitly provides a baseline or threshold. If no baseline exists, describe the observation without interpreting its magnitude.

NO BASELINE IS PROVIDED SO DON'T classify something as high, low or normal, that is not allowed.

Do NOT recommend investigations.

Do NOT compare behavioural observations with the current flow.

Do NOT use cybersecurity knowledge that is not explicitly present in the behavioural observations.

If the behavioural observations are consistent with the prediction, answer Supports.

If some observations support while others weaken it, answer Partially Supports.

If the behavioural observations clearly conflict with the prediction, answer Contradicts.

If there are no behavioural observations relevant to the prediction, answer Insufficient Evidence.

If seeing the evidence, you think that the Agent 1 is not right kindly don't blindly follow it.

Return ONLY:

Verdict:
Supports
Partially Supports
Contradicts
Insufficient Evidence

Evidence Used:
You have to briefly tell evidence you used to support or contradict Agent 1 and it is necessary you keep it brief and use only the data given.

Reason:
Exactly one sentence and don't say things like it aligns or doesn't to that specific threat type.
Reference ONLY the behavioural observations.
Do not mention the current flow.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        },
    )

    return response.json()["response"]

if verdict in ["Supports","Partially Supports"]:
    history.record(ip,prediction,confidence)
    historical_activity=history.lookup(ip)

# ============================================================
# PIPELINE
# ============================================================

def run_pipeline(flow_data, builder):

    print("\n" + "=" * 60)
    print("INCOMING FLOW")
    print("=" * 60)

    X = flow_data[rf_features]
    print("Flow data shape:", flow_data.shape)
    print(flow_data)

    print("RF features:")
    print(rf_features)
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

    # -------------------------
    # Agent 1
    # -------------------------
    print(X)
    print(X.shape)
    prediction = rf_model.predict(X)[0]
    probability = rf_model.predict_proba(X)[0]
    confidence = float(max(probability) * 100)

    class_probs = dict(zip(rf_model.classes_, probability))

    sorted_probs = sorted(class_probs.items(), key=lambda x: x[1], reverse=True)

    print(f"\nAgent 1 Decision: {prediction}")
    print(f"Confidence: {confidence:.2f}%")

    print("\nTop Predictions:")
    for cls, prob in sorted_probs[:3]:
        print(f"{cls:<25} {prob*100:.2f}%")

    if prediction == "BENIGN":
    print("\n✅ Flow is BENIGN — pipeline stops here.")

    return {
        "prediction": prediction,
        "confidence": confidence,
        "structured_data": None,
        "agent2_result": None,
        "agent3_report": None
    }

    print("\n⚠️ Suspicious flow detected.")
    print("Building context for Agent 2...\n")

    # -------------------------
    # Context Builder
    # -------------------------
    context = builder.build_context(
        flow_data,
        prediction,
        confidence,
        class_probs
    )

    # -------------------------
    # Structured + Brief inputs
    # -------------------------

    structured_data = {
         "agent1_summary": context["agent1_summary"],
         "current_flow": context["current_flow"],
         "behaviour_summary": context["behaviour_summary"],
         "all_predictions": class_probs
     }

    context_brief = build_context_brief(context)


    
    # -------------------------
    # Debug print
    # -------------------------
    print("STRUCTURED DATA SENT TO AGENT 2:\n")
    print(json.dumps(structured_data, indent=2))

    print("\nCONTEXT BRIEF SENT TO AGENT 2:\n")
    print(context_brief)

    print("\n--- Agent 2 Response ---\n")

    # -------------------------
    # Agent 2
    # -------------------------
    result = agent2_analyze(structured_data, context_brief)

    print(result)

    verdict = None

    for line in result.splitlines():

    line = line.strip()

    if line in [
        "Supports",
        "Partially Supports",
        "Contradicts",
        "Insufficient Evidence"
    ]:
        verdict = line
        break


    historical_activity = None

    if verdict in ["Supports", "Partially Supports"]:

        ip = flow_data.iloc[0]["Source IP"]

        history.record(
            ip,
            prediction,
            confidence
        )

        historical_activity = history.lookup(ip)

    print("\n--- Agent 3 Report ---\n")

    report = agent3_generate_report(
    agent1_summary=structured_data["agent1_summary"],
    current_flow=structured_data["current_flow"],
    agent2_result=result,
    historical_activity=historical_activity
    )

    print(report)

    # -------------------------
    # Save incident
    # -------------------------
    with open("incident_reports.txt", "a", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Agent 1: {prediction} ({confidence:.2f}%)\n")
        f.write("-" * 60 + "\n")
        f.write(json.dumps(structured_data, indent=2))
        f.write("\n\n")
        f.write(context_brief)
        f.write("\n\n")
        f.write(report)
        f.write("\n\n")

    return result


# ============================================================
# DATA LOADING
# ============================================================

print("\nLoading test data...")

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

builder = ContextBuilder(df)


# ============================================================
# TEST RUNS
# ============================================================

print("\n" + "=" * 60)
print("TEST 1 : Known DDoS Flow")

ddos_flow = df[df["Label"] == "DDoS"].head(1)
run_pipeline(ddos_flow, builder)


print("\n" + "=" * 60)
print("TEST 2 : Known BENIGN Flow")

benign_flow = df[df["Label"] == "BENIGN"].head(1)
run_pipeline(benign_flow, builder)


print("\n" + "=" * 60)
print("TEST 3 : Random Flow")

random_flow = df.sample(1)
actual_label = random_flow["Label"].values[0]

run_pipeline(random_flow, builder)

print(f"\nGround Truth: {actual_label}")