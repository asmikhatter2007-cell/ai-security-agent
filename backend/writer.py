import requests
import json


def agent3_generate_report(report_data):

    prompt = f"""
You are Agent 3.

Here is a completed SOC incident report.

Do NOT modify any information.

Write ONLY an Executive Summary.

Requirements:
- 3-4 sentences
- Professional SOC language.
- Mention:
-Classification
-Agent2 verdict
-historical activity(if available)
-recommendation

-Do not invent facts
-Return ONLY the executive summary

Report:

{json.dumps(report_data,indent=2)}

"""

   
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "num_predict": 120
            }
        },
        timeout=15
    )

    summary = response.json()["response"]
    return summary