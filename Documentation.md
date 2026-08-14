HackBlock

Project Overview:
HackBlock, an AI Security Agent is a multi-agent SOC that combines ML, Context-Builder, LLM and a report generator to predict a cybersecurity threat and generate a report consisting of result, evidence,reason, recommendation and a summary.

Motivation:
The main motive was to make something in the domain of cybersecurity to explore my interests and this idea seemed to be most appealing because-
1. Many SOC Analysts spend their time detecting threats manually.
2. Existing ML models only classify and many solutions use thresholds for detecting threats.
3. LLM integration was still an ongoing process and generally they hallucinate because of their pre-existing knowledge.


Architecture-
1. **Agent1**- A fast ML based filter(Random Forest)which scans the logs and flags suspicious network flows through finding patterns in the data.

2. **Context-Builder**- This layer converts raw network logs into behavioural summaries. It plays an important role because an LLM needs richer context to analyze evidence reach a verdict.

3. **Agent2**- This part consists of an LLM whose task is to not detect a threat but to support or disagree with the Agent1's prediction. This architecture was adapted to prevent irrelevant results.

4. **Agent3**- The main task of this layer is to prepare a report based on the results of Agent 1 and Agent 2. It gives evidence used, recommendation, summary and reason.

Pipeline-

Network Traffic --> Agent 1(Random Forest) --> Context Builder(Behaviour Summary) --> Agent 2(Qwen2.5) --> Agent 3(SOC Report)

1. Agent 1-



* Random Forest

* Filter layer

* Gives confidence score

2. Context Builder-



* Generates a behaviour summary from network flows.

* Includes historical data in creating richer context.

3. Agent 2-



* Validates Agent 1 results.

Designed in consideration of-

* Hallucination reduction

* Structured prompt

* Behavioural priorities

* Prevent new evidence creation

* Do not classify threats

4. Agent 3-



It Converts technical observations to-

* executive summary

* SOC report

Tech Stack-

Frontend-

1. React


2. Vite


3. Tailwind CSS



Backend-

1. FastAPI


2. Python



ML-

1. Random Forest


2. Scikit-learn



LLM-

1. Ollama QWEN 2.5(7B) is choosen as the LLM that is locally deployed.


2. Python(Pandas) is used for data analysis.


3. VS Code and Git for version control.



Intentional design choice-ML + LLM Reasoning-

1. Accuracy- In ML systems one can almost not predict why a log was flagged or what the logic behind it was. In order to prevent that we used the rule based approach with an LLM reasoning.


2. Acknowledged tradeoff- A trained ML system would probably have a higher accuracy on this same task- this is an intentional decision.



Threats detection-

1. Brute Force- multiple failed logins from a single IP address.


2. Port Scan- scan all the ports to detect which are the ones exchanging data and which are idle.


3. DDoS- high request volume from different IPs.


Yet to build-

4. Unusual Geographical Access- login from a unexpected location for a given user.


5. Data Exfiltration- unusuall large amount of data exchange at an unusual time.



Dataset-

CICIDS 2017(Canadian Institute for Cybersecurity)- real, labelled, research-grade network flow data.

Features-

1. Multi-agent


2. Explainable AI


3. Dashboard


4. Live Feed


5. Recent Incidents


6. Analyst Reports
## Model Performance(Agent-1 Random Forest)
Evaluated on a test set of 3,65,911 flows from CICIDS2017.

                             precision    recall  f1-score   support

                    BENIGN       1.00      1.00      1.00    254383
                       Bot       0.82      0.78      0.80       393
                      DDoS       1.00      1.00      1.00     25606
             DoS GoldenEye       0.98      0.98      0.98      2059
                  DoS Hulk       1.00      1.00      1.00     46215
          DoS Slowhttptest       0.99      0.99      0.99      1100
             DoS slowloris       1.00      0.99      0.99      1159
               FTP-Patator       1.00      1.00      1.00      1588
              Infiltration       1.00      0.57      0.73         7
                  PortScan       0.99      1.00      1.00     31785
               SSH-Patator       1.00      1.00      1.00      1179
    Web Attack Brute Force       0.32      0.29      0.30       301
  Web Attack Sql Injection       1.00      0.50      0.67         4
            Web Attack XSS       0.08      0.06      0.07       130

                  accuracy                           1.00    365911
                 macro avg       0.88      0.81      0.83    365911
              weighted avg       1.00      1.00      1.00    365911

### Notes on evaluation

The model performs near-perfectly on the classes- DDoS,Portscan,brute-force variants,and DoS types, which are the primary detection targets of this system.

The gap between the weighted average(1.00) and macro average(0.83) is expected because weighted average is dominated by BENIGN traffic, which makes up almost 70% of test set, so it makes weaker performance on rare classes. Web attack subclasses(XSS, SQL Injection) have very low support in CICIDS2017 and the model underperforms there which is class-imbalance limitation. 

              

