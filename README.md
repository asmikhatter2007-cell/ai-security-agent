# AI Security Agent

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
- LLM: Ollama Qwen2.5(7B)

##Setup
###Backend
\`\`\`
cd backend
pip install -r requirements.txt
uvicorn server:app --reload
\`\`\`
###Frontend
\`\`\`
cd frontend
npm install
npm run dev
\`\`\`

## Dataset
CICIDS 2017(Canadian Institute for Cybersecurity)-real, lebelled, research-grade network flow data.

## Project Structure


