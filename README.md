# HackBlock

HackBlock, is a multi-agent SOC assistant that combines Machine Learning Classifier, a Context-Builder, an LLM-based behavioural validation and a Python based SOC report formatter to predict a cybersecurity threat and generate a report consisting of result, evidence, reason, recommendation, historical activity and a summary.

The system provides:

- Threat classification
- Confidence estimation
- Behavioural evidence
- LLM-based behavioural validation
- Historical activity
- Analyst-oriented recommendations
- Live threat monitoring
- Structured SOC incident reports

HackBlock Dashboard<img width="950" height="427" alt="image" src="https://github.com/user-attachments/assets/2af754c4-6072-44ea-bcc6-37c9a3f4f121" />


## How it works
1. **Agent 1**- A fast ML based filter(Random Forest)which scans the logs and flags suspicious network flows through finding patterns in the data.

2. **Context-Builder**- This layer converts raw network logs into behavioural summaries. It plays an important role because an LLM needs richer context to analyze evidence and reach a verdict.

3. **Agent 2**- This part consists of an LLM whose task is to not detect a threat but to support or disagree with the Agent1's prediction. This architecture was adapted to prevent irrelevant results.

Designed with:

- Structured prompting
- Behavioural evidence prioritization
- Hallucination reduction
- Evidence-only reasoning
- No independent threat classification
- No new evidence generation
  
4. **Agent 3** - A deterministic Python-based formatting layer that converts the outputs of Agent 1 and Agent 2 into a structured SOC incident report.

The report contains:

- Executive Summary
- Classification
- Confidence
- Agent 2 Verdict
- Reason
- Evidence
- Historical Activity
- Recommendation
  
## Features
1. Multi-agent
2. Explainable-AI
3. Dashboard
4. Live Feed
5. Recent Incidents
6. Analyst Reports

Agent 3 Incident Report
<img width="930" height="414" alt="image" src="https://github.com/user-attachments/assets/ff95945d-5464-4779-844b-4297371305ab" />
<img width="935" height="406" alt="image" src="https://github.com/user-attachments/assets/ef1791e5-be1f-4962-88bf-8c47f7165116" />
<img width="932" height="404" alt="image" src="https://github.com/user-attachments/assets/5506560b-4f12-4929-9e17-04860a8eb711" />



   

## Tech stack
- Frontend: React, Vite, Tailwind CSS
- Backend: FastAPI, Python
- ML: Random Forest, Scikit-learn
- LLM: Ollama Qwen2.5(7B for Agent 2)
- Incident Report: Python-based deterministic formatter
  
## Setup
### Backend
cd backend
<br>
pip install -r requirements.txt
<br>
uvicorn server:app --reload

### Frontend
cd frontend
<br>
npm install
<br>
npm run dev

## Dataset
CICIDS 2017(Canadian Institute for Cybersecurity)-real, labelled, research-grade network flow data.

## Project Structure

````
hackblock/
├── backend/              # FastAPI server + ML/LLM pipeline
│   ├── server.py         # API entry point (routes: /predict, /next-flow, /generate-report)
│   ├── pipeline_core.py  # Core detection pipeline (Agent 1 → Context Builder -> Agent 2)
│   ├── context_builder.py# Builds SOC context brief for the LLM
│   ├── historical_activity.py
│   ├── requirements.txt
│   ├── rf_model.pkl      # Trained Random Forest model (Agent 1)
│   ├── rf_features.pkl   # Feature list used by the model
│   └── dataset/          # CICIDS2017 CSVs (not tracked in git)
│
├── frontend/              # React + Vite dashboard
│   ├── src/
│   │   ├── components/    # UI components (LiveFeed, ThreatCard, Sidebar, etc.)
│   │   ├── api/            # Calls to the backend API
│   │   └── App.jsx
│   └── package.json
│
├── exploration/           # Early data-analysis scripts (kept for reference)
│   ├── analyze_columns.py
│   ├── explore_data.py
│   └── unsw.py
│
├── rf_train.py            # Trains the Random Forest model (Agent 1)
├── test_agent.py          # Test script for the pipeline
├── thresholds.json        # Detection thresholds config
├── Documentation.md        # Architecture & design notes
└── README.md
````
