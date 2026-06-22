AI-Security-Agent

Project Overview
Multi-agent AI system for cloud/network security incident detection with the main purpose to explore different domains and build something useful from scratch.

Architecture-
1. **Agent1**- A fast statistical filter(rule based) which scans the logs and flags suspicious values using hardcoded rules which adapt to dataset's own baseline.

2. **Agent2**- This is the reasoning layer where the agent distinguishes between the threats and recommend actions.

3. **Agent3**-Planned not yet built. It will be most probably the response layer.

Tech Stack-
1. Ollama QWEN 2.5(7B) is choosen as the LLM that is locally deployed.
2. Python(Pandas) is used for data analysis.
3. VS Code and Git for version control.

Intentional design choice-Rule Based + LLM Reasoning not an ML-
1. **Explainable**- In ML systems one can almost not predict why a log was flagged or what the logic behind it was. In order to prevent that we used the rule based approach with an LLM reasoning.

2. **Acknowledged tradeoff**- A trained ML system would probably have a higher accuracy on this same task- this is an intentional decision.

Threats detection-
1. **Brute Force**- multiple failed logins from a single IP address.
2. **Port Scan**- scan all the ports to detect which are the ones exchanging data and which are idle.
3. **DDoS**- high request volume from different IPs- not yet tested.
4. **Unusual Geographical Access**- login from a unexpected location for a given user.
5. **Data Exfiltration**- unusuall large amount of data exchange at an unusual time.

Dataset-
CICIDS 2017(Canadian Institute for Cybersecurity)- real, labelled, research-grade network flow data.