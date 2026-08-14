# HackBlock

HackBlock, an AI Security Agent is a multi-agent SOC that combines ML, Context-Builder, LLM and a report generator to predict a cybersecurity threat and generate a report consisting of result, evidence,reason, recommendation and a summary.

## How it works
1. **Agent 1**- A fast ML based filter(Random Forest)which scans the logs and flags suspicious network flows through finding patterns in the data.

2. **Context-Builder**- This layer converts raw network logs into behavioural summaries. It plays an important role because an LLM needs richer context to analyze evidence reach a verdict.

3. **Agent 2**- This part consists of an LLM whose task is to not detect a threat but to support or disagree with the Agent1's prediction. This architecture was adapted to prevent irrelevant results.

4. **Agent 3**- The main task of this layer is to prepare a report based on the results of Agent 1 and Agent 2. It gives evidence used, recommendation, summary and reason.

## Features
1. Multi-agent
2. Explainable-AI
3. Dashboard
4. Live Feed
5. Recent Incidents
6. Analyst Reports

## Tech stack
- Frontend: React, Vite, Tailwind CSS
- Backend: FastAPI, Python
- ML: Random Forest, Scikit-learn
- LLM: Ollama Qwen2.5(7B for Agent 2 and 3B for Agent 3)

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
CICIDS 2017(Canadian Institute for Cybersecurity)-real, lebelled, research-grade network flow data.

## Project Structure

````
ai-security-agent/
├── backend/              # FastAPI server + ML/LLM pipeline
│   ├── server.py         # API entry point (routes: /predict, /next-flow, /generate-report)
│   ├── pipeline_core.py  # Core detection pipeline (Agent 1 → Agent 2 → Agent 3)
│   ├── context_builder.py# Builds SOC context brief for the LLM
│   ├── historical_activity.py
│   ├── writer.py         # Agent 3 — generates the final incident report
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
