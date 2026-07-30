import requests
import json


def agent3_generate_report(agent1_summary,
                           current_flow,
                           agent2_result,historical_activity=None):

    prompt = f"""
You are Agent 3 of a multi-agent SOC assistant.

You are NOT allowed to perform intrusion detection.

Agent 1 has already classified the traffic.
Agent 2 has already validated whether the behavioural evidence supports that prediction.

Your job is ONLY to produce a professional SOC incident report.

Use ONLY the information supplied below.

Do NOT invent facts.
Do NOT change Agent 1's prediction.
Do NOT change Agent 2's verdict.
Do NOT estimate attack severity.
Do NOT estimate confidence.
Do NOT introduce cybersecurity knowledge that is not explicitly present.

Information Available

Agent 1:
{json.dumps(agent1_summary, indent=2)}

Current Flow:
{json.dumps(current_flow, indent=2)}

Agent 2 Result:
{agent2_result}

Historical Activity:
{json.dumps(historical_activity,indent=2) if historical_activity else "Not Available"}

Generate the report using EXACTLY this structure.

Classification:
<Agent 1 prediction>

Confidence:
<Agent 1 confidence>

Source:
<Source IP>

Destination:
<Destination IP>

Verdict:
<Agent 2 verdict>

Evidence:
<List ONLY the evidence reported by Agent 2 as bullet points. Do not rewrite or add new evidence.>

Reason:
<Copy the reasoning from Agent 2 in one sentence.>

Historical Activity:
If historical activity is available, add a separate section called
Historical Activity

Include only:

1. First seen
2. Last seen
3. Previous Validated Incidents
4. Attack History

Do not analyse it.

Do not use it as evidence.

Do not change the recommendation because of it.

Only report the information.

Write ONE recommendation based ONLY on Agent 2's verdict.

Supports
→ Escalate this incident for SOC analyst review.

Partially Supports
→ Review additional telemetry before escalation.

Contradicts
→ Revalidate the prediction using additional evidence.

Insufficient Evidence
→ Collect more behavioural data before making a decision.

Do not recommend blocking traffic.
Do not recommend containment.
Do not recommend remediation.
Do not recommend investigation steps beyond the sentence above.

Write exactly 3-4 concise statements that summarize:
- the prediction,
- the behavioural verification outcome,
- and the recommendation.

The summary must not introduce any new technical information.

It must sound professional and clean, not a copy paste of Agent 2 result.

It must also summarise the prediction of Agent 1 and Agent 2 in one line each.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        },
        timeout=120
    )

    return response.json()["response"]