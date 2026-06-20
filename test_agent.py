import requests
import json

def analyze_log(log_entry):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            "model": "qwen2.5:7b",
            "prompt": f"""You are a cybersecurity analyst. Analyze this log entry ONLY for these patterns:
- 5+ failed logins from same IP/user within 60 seconds = Brute Force
- 500+ requests within 1 second from multiple IPs = DDoS
- Same IP trying 10+ different ports within 30 seconds = Port Scan
- 500MB+ data downloaded within 10 minutes outside business hours = Data Exfiltration

If none of these patterns match clearly, say "No clear threat detected."

Return your answer in this exact format:
Threat: [name or "None"]
Severity: [HIGH/MEDIUM/LOW/NONE]
Confidence: [percentage]
Recommended Action: [specific action]

Log entry:
{log_entry}""",
            "stream": False
        }
    )
    result = response.json()
    return result['response']

# Multiple test logs - different attack types
test_logs = {
    "Brute Force": """
2026-06-18 11:23:41 - Failed login - User: admin - IP: 185.234.219.57 - Attempt 1
2026-06-18 11:23:42 - Failed login - User: admin - IP: 185.234.219.57 - Attempt 2
2026-06-18 11:23:43 - Failed login - User: admin - IP: 185.234.219.57 - Attempt 3
2026-06-18 11:23:44 - Failed login - User: admin - IP: 185.234.219.57 - Attempt 4
2026-06-18 11:23:45 - Failed login - User: admin - IP: 185.234.219.57 - Attempt 5
2026-06-18 11:23:46 - Failed login - User: admin - IP: 185.234.219.57 - Attempt 6
""",
    "Port Scan": """
2026-06-18 16:12:01 - Connection attempt - Port: 21 - IP: 45.33.32.156 - Failed
2026-06-18 16:12:02 - Connection attempt - Port: 22 - IP: 45.33.32.156 - Failed
2026-06-18 16:12:03 - Connection attempt - Port: 23 - IP: 45.33.32.156 - Failed
2026-06-18 16:12:04 - Connection attempt - Port: 80 - IP: 45.33.32.156 - Failed
2026-06-18 16:12:05 - Connection attempt - Port: 443 - IP: 45.33.32.156 - Failed
2026-06-18 16:12:06 - Connection attempt - Port: 3389 - IP: 45.33.32.156 - Failed
2026-06-18 16:12:07 - Connection attempt - Port: 8080 - IP: 45.33.32.156 - Failed
2026-06-18 16:12:08 - Connection attempt - Port: 8443 - IP: 45.33.32.156 - Failed
2026-06-18 16:12:09 - Connection attempt - Port: 3306 - IP: 45.33.32.156 - Failed
2026-06-18 16:12:10 - Connection attempt - Port: 5432 - IP: 45.33.32.156 - Failed
""",
    "Normal Traffic": """
2026-06-18 09:15:23 - User john logged in successfully - IP: 203.45.67.89
2026-06-18 09:15:45 - File accessed: homepage.html - IP: 203.45.67.89
2026-06-18 09:16:02 - API request made - IP: 203.45.67.89 - Response: 200 OK
2026-06-18 09:17:30 - User john logged out - IP: 203.45.67.89
"""
}

for threat_type, log in test_logs.items():
    print(f"\n{'='*50}")
    print(f"Testing: {threat_type}")
    print('='*50)
    result = analyze_log(log)
    print(result)

