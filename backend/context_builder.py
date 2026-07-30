import pandas as pd


class ContextBuilder:

    HISTORY_SIZE = 50
    WINDOW_SECONDS = 30

    def __init__(self, dataset):
        self.df = dataset.copy()

        print("Building Source IP history index...")

        self.history_lookup = {}

        grouped = self.df.groupby("Source IP")

        for ip, group in grouped:
            self.history_lookup[ip] = group.tail(self.HISTORY_SIZE)

        print(f"Indexed {len(self.history_lookup)} Source IPs.")

    # ==========================================================
    # MAIN FUNCTION
    # ==========================================================

    def build_context(self, flow, prediction, confidence, class_probs):

        context = {}

        # --------------------------
        # Agent 1 Summary
        # --------------------------

        top_predictions = sorted(
            class_probs.items(),
            key=lambda x: x[1],
            reverse=True
        )[:2]

        context["agent1_summary"] = {
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "top_predictions": [
                {
                    "class": cls,
                    "probability": round(prob * 100, 2)
                }
                for cls, prob in top_predictions
            ]
        }

        # --------------------------
        # Current Flow
        # --------------------------

        important_columns = [

            "Source IP",
            "Destination IP",
           # "Source Port",
            #"Destination Port",
            #"Protocol",
           

            #"Flow Duration",

            "Total Fwd Packets",
            "Total Backward Packets",

            "Total Length of Fwd Packets",

            #"Flow Bytes/s",
            #"Flow Packets/s",

            "SYN Flag Count",
            "ACK Flag Count",
            "RST Flag Count",

            #"Init_Win_bytes_forward"

        ]

        available = [
            c for c in important_columns
            if c in self.df.columns
        ]

        context["current_flow"] = (
            flow[available]
            .iloc[0]
            .to_dict()
        )

        # --------------------------
        # Source History
        # --------------------------
        
        source_ip = flow.iloc[0]["Source IP"]

        history = self.history_lookup.get(
        source_ip,
        pd.DataFrame(columns=self.df.columns)
)


        context["behaviour_summary"] = {
        "history_scope": {
        "description": "These observations summarize recent behaviour from the same Source IP. They provide behavioural evidence and are not expected to exactly match the current flow.",
        "history_size": len(history)
        },
        "evidence_from_recent_activity": {}
       }

        for cls, _ in top_predictions:

            if cls == "PortScan":

                context["behaviour_summary"]["evidence_from_recent_activity"] = \
                    self.portscan_summary(history)

            elif cls in ["DDoS","DoS Hulk","DoS GoldenEye","DoS Slowhttptest","DoS slowloris"]:

                context["behaviour_summary"]["evidence_from_recent_activity"] = \
                    self.ddos_summary(history)

            elif cls in ["Brute Force", "FTP-Patator", "SSH-Patator"]:

                context["behaviour_summary"]["evidence_from_recent_activity"] = \
                    self.bruteforce_summary(history)
           

        return context

    # ==========================================================
    # PORTSCAN
    # ==========================================================
    def portscan_summary(self, history):

        observations = {}

        observations["history_window"] = int(len(history))

        observations["flows_observed"] = int(len(history))

        observations["same_destination_ip"] = bool(
        history["Destination IP"].nunique() == 1
    )
        observations["unique_destination_ports"] = int(
        history["Destination Port"].nunique()
    )

        observations["repeated_connections_to_same_host"] = bool(
        history["Destination IP"]
        .value_counts()
        .max() > 10
    )

        observations["time_span_seconds"] = self.WINDOW_SECONDS

        observations["average_gap_between_flows"] = round(
        self.WINDOW_SECONDS / max(len(history), 1),
        2
    )

        avg_payload = history["Total Length of Fwd Packets"].mean()

        if avg_payload < 100:
            observations["payload_characteristic"] = "very small payloads"

        elif avg_payload < 1000:
            observations["payload_characteristic"] = "medium payloads"

        else:
            observations["payload_characteristic"] = "large payloads"

        return observations


    def ddos_summary(self, history):

        observations = {}

        observations["history_window"] = len(history)

        observations["flows_observed"] = len(history)

        observations["same_destination_ip"] = bool(
        history["Destination IP"].nunique() == 1
    )
        top_destination = history["Destination IP"].value_counts()

        most_targeted_ip = top_destination.index[0]
        flows_to_top_destination = int(top_destination.iloc[0])

        observations["destination_concentration"] = {
        "most_targeted_destination": most_targeted_ip,
        "flows_to_destination": flows_to_top_destination,
        "total_flows": len(history)
    }

        observations["average_forward_packets"] = round(
        history["Total Fwd Packets"].mean(),
        2
    )

        observations["payload_characteristic"] = (
        "very small payloads"
        if history["Total Length of Fwd Packets"].mean() < 100
        else "medium/large payloads"
    )

        observations["time_span_seconds"] = self.WINDOW_SECONDS

        observations["average_gap_between_flows"] = round(
        self.WINDOW_SECONDS / max(len(history), 1),
        2
    )

# -------------------------
# NEW OBSERVATIONS
# -------------------------


        observations["request_frequency"] = round(
        len(history) / self.WINDOW_SECONDS,
        2
    )
        top_port = history["Destination Port"].value_counts()

        observations["most_targeted_port"] = {
        "port": int(top_port.index[0]),
        "flows": int(top_port.iloc[0])
    }

        observations["source_destination_distribution"] = {
        "unique_source_ips": int(history["Source IP"].nunique()),
        "unique_destination_ips": int(history["Destination IP"].nunique())
    }

        return observations
    # ==========================================================
    # BRUTE FORCE
    # ==========================================================

    def bruteforce_summary(self, history):

        auth_ports = [
            21,
            22,
            23,
            3389,
            445
        ]

        auth_history = history[
            history["Destination Port"].isin(auth_ports)
        ]

        return {

            "recent_flows":
                int(len(history)),

            "authentication_port_seen":
                bool(len(auth_history) > 0),

            "unique_authentication_ports":
                int(
                    auth_history[
                        "Destination Port"
                    ].nunique()
                ),

            "connections_to_same_destination":

                int(
                    history[
                        "Destination IP"
                    ]
                    .value_counts()
                    .max()
                ),

            "average_flow_duration":

                round(
                    history[
                        "Flow Duration"
                    ].mean(),
                    2
                )
        }