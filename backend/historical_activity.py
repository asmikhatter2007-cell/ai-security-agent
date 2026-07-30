import json
import os
from datetime import datetime

MEMORY_FILE = "historical_activity.json"


class HistoricalActivity:

    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                self.data = json.load(f)

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def record(self, ip, attack, confidence):

        if ip not in self.data:
            self.data[ip] = {
                "first_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_seen": "",
                "validated_incidents": 0,
                "threat_counts": {},
                "last_prediction": "",
                "last_confidence": 0,
                "recent_history": []
            }

        record = self.data[ip]

        record["validated_incidents"] += 1
        record["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record["last_prediction"] = attack
        record["last_confidence"] = round(confidence, 2)

        record["threat_counts"][attack] = (
            record["threat_counts"].get(attack, 0) + 1
        )

        record["recent_history"].append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prediction":attack,
            "confidence":round(confidence,2)
        })
        record["recent_history"]=record["recent_history"][-50:]
        self.save()

   
    def lookup(self, ip):

        return self.data.get(ip, None)