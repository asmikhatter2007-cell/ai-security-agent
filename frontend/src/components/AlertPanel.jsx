const THREAT_COLORS = {
  PortScan: "#F97316",
  DDoS: "#EF4444",
  "Brute Force": "#A855F7",
};

export default function AlertPanel({ alerts = [] }) {
  return (
    <div className="alert-panel">
      <div style={{
        fontSize: 10,
        color: "#7C8CA5",
        letterSpacing: "0.1em",
        textTransform: "uppercase",
        marginBottom: 20,
      }}>
        Recent Incidents
      </div>

      {alerts.length === 0 ? (
        <div style={{
          color: "#1E3A5F",
          fontSize: 12,
          textAlign: "center",
          padding: "40px 0",
          fontFamily: "'JetBrains Mono', monospace",
        }}>
          No incidents yet
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {alerts.map((alert, i) => {
            const color = THREAT_COLORS[alert.threat] || "#7C8CA5";
            return (
              <div key={alert.id + i} style={{
                background: "#060E1A",
                border: `1px solid ${color}30`,
                borderLeft: `3px solid ${color}`,
                borderRadius: 8,
                padding: "10px 12px",
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                  <span style={{ color, fontSize: 12, fontWeight: 700 }}>
                    {alert.threat}
                  </span>
                  <span style={{
                    fontSize: 10,
                    color: alert.severity === "HIGH" ? "#EF4444" : "#F59E0B",
                    fontWeight: 600,
                  }}>
                    {alert.severity}
                  </span>
                </div>
                <div style={{
                  fontFamily: "'JetBrains Mono', monospace",
                  color: "#7C8CA5",
                  fontSize: 11,
                  marginBottom: 4,
                }}>
                  {alert.srcIp}
                </div>
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                  <span style={{
                    fontSize: 10,
                    color: alert.verdict === "Supports" ? "#10B981" : "#F59E0B",
                  }}>
                    {alert.verdict}
                  </span>
                  <span style={{ fontSize: 10, color: "#7C8CA5", fontFamily: "monospace" }}>
                    {alert.timestamp}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}