import { useState, useEffect, useRef } from "react";

const THREAT_COLORS = {
  BENIGN: "#10B981",
  PortScan: "#F97316",
  DDoS: "#EF4444",
  "Brute Force": "#A855F7",
};

const THREAT_ICONS = {
  BENIGN: "✓",
  PortScan: "⚠",
  DDoS: "🚨",
  "Brute Force": "⚠",
};

function FlowCard({ flow, onExpire }) {
  const [visible, setVisible] = useState(true);
  const [expanded, setExpanded] = useState(!flow.isBenign);
  const [opacity, setOpacity] = useState(1);

  useEffect(() => {
    if (flow.isBenign) {
      const fadeTimer = setTimeout(() => {
        setOpacity(0);
      }, 5000);
      const removeTimer = setTimeout(() => {
        setVisible(false);
        onExpire && onExpire(flow.id);
      }, 6000);
      return () => {
        clearTimeout(fadeTimer);
        clearTimeout(removeTimer);
      };
    }
  }, [flow.isBenign]);

  if (!visible) return null;

  const color = THREAT_COLORS[flow.threat] || "#6B7280";
  const icon = THREAT_ICONS[flow.threat] || "?";

  return (
    <div
      onClick={() => !flow.isBenign && setExpanded(e => !e)}
      style={{
        opacity,
        transition: "opacity 1s ease, transform 0.3s ease",
        background: flow.isBenign
          ? "rgba(16,185,129,0.04)"
          : `rgba(${flow.threat === "DDoS" ? "239,68,68" : flow.threat === "PortScan" ? "249,115,22" : "168,85,247"},0.08)`,
        border: `1px solid ${color}${flow.isBenign ? "20" : "40"}`,
        borderLeft: `3px solid ${color}`,
        borderRadius: 10,
        padding: flow.isBenign ? "8px 14px" : "14px 16px",
        marginBottom: 8,
        cursor: flow.isBenign ? "default" : "pointer",
        transition: "all 0.3s ease",
      }}
    >
      {/* Main row */}
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <span style={{
          color,
          fontSize: flow.isBenign ? 12 : 16,
          fontWeight: 700,
          minWidth: 20,
          textAlign: "center",
        }}>
          {icon}
        </span>

        <div style={{ flex: 1 }}>
          <div style={{
            color: flow.isBenign ? "#6B7280" : "#E5E7EB",
            fontSize: flow.isBenign ? 12 : 14,
            fontWeight: flow.isBenign ? 400 : 700,
            letterSpacing: "0.04em",
          }}>
            {flow.threat}
          </div>
          <div style={{
            fontFamily: "'JetBrains Mono', monospace",
            color: "#94A3B8",
            fontSize: 11,
            marginTop: 2,
          }}>
            {flow.srcIp} → {flow.dstIp}
          </div>
        </div>

        <div style={{
          fontFamily: "'JetBrains Mono', monospace",
          color,
          fontSize: 13,
          fontWeight: 600,
          minWidth: 45,
          textAlign: "right",
        }}>
          {flow.confidence}%
        </div>

        <div style={{
          fontFamily: "'JetBrains Mono', monospace",
          color: "#1F2937",
          fontSize: 10,
          minWidth: 55,
          textAlign: "right",
        }}>
          {flow.timestamp}
        </div>
      </div>

      {/* Expanded Agent 2 verdict — only for threats */}
      {!flow.isBenign && expanded && (
        <div style={{
          marginTop: 12,
          padding: "10px 12px",
          background: "rgba(0,0,0,0.3)",
          borderRadius: 8,
          borderLeft: `2px solid ${color}`,
        }}>
          <div style={{ display: "flex", gap: 20, marginBottom: 8 }}>
            <div>
              <div style={{ fontSize: 10, color: "#4B5563", letterSpacing: "0.08em", marginBottom: 3 }}>
                AGENT 2 VERDICT
              </div>
              <div style={{
                color: flow.verdict === "Supports" ? "#10B981" : "#F59E0B",
                fontSize: 12,
                fontWeight: 600,
              }}>
                {flow.verdict}
              </div>
            </div>
            <div>
              <div style={{ fontSize: 10, color: "#4B5563", letterSpacing: "0.08em", marginBottom: 3 }}>
                SEVERITY
              </div>
              <div style={{
                color: flow.severity === "HIGH" ? "#EF4444" : flow.severity === "MEDIUM" ? "#F59E0B" : "#10B981",
                fontSize: 12,
                fontWeight: 600,
              }}>
                {flow.severity}
              </div>
            </div>
          </div>
          <div style={{ color: "#6B7280", fontSize: 12, lineHeight: 1.6 }}>
            {flow.reason}
          </div>
        </div>
      )}
    </div>
  );
}

// Simulate flows — replace with real pipeline data later
function generateFlow() {
  const isBenign = Math.random() < 0.7;
  const threats = ["PortScan", "DDoS", "Brute Force"];
  const threat = isBenign ? "BENIGN" : threats[Math.floor(Math.random() * threats.length)];
  const srcIPs = ["172.16.0.1", "185.234.219.57", "45.33.32.156", "10.0.0.47"];
  const dstIPs = ["192.168.10.50", "192.168.10.51", "10.0.0.1"];

  return {
    id: Math.random().toString(36).substr(2, 8),
    timestamp: new Date().toLocaleTimeString("en-GB", { hour12: false }),
    srcIp: srcIPs[Math.floor(Math.random() * srcIPs.length)],
    dstIp: dstIPs[Math.floor(Math.random() * dstIPs.length)],
    threat,
    isBenign,
    confidence: isBenign ? 95 + Math.floor(Math.random() * 6) : 75 + Math.floor(Math.random() * 26),
    verdict: isBenign ? null : Math.random() > 0.2 ? "Supports" : "Partially Supports",
    severity: isBenign ? null : Math.random() > 0.5 ? "HIGH" : "MEDIUM",
    reason: isBenign ? null : threat === "PortScan"
      ? `${30 + Math.floor(Math.random() * 20)} unique destination ports across 50 recent flows is consistent with systematic port scanning behavior.`
      : threat === "DDoS"
      ? `${(1.5 + Math.random()).toFixed(2)} flows/sec with small average payloads is consistent with volumetric flooding behavior.`
      : `${20 + Math.floor(Math.random() * 30)} repeated connections to same destination with authentication port activity detected.`,
  };
}

export default function LiveFeed({ onNewThreat, onStatsUpdate }) {
  const [flows, setFlows] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      const flow = generateFlow();

      setFlows(prev => [flow, ...prev].slice(0, 50));

      if (!flow.isBenign && onNewThreat) {
        onNewThreat(flow);
      }

      if (onStatsUpdate) {
        onStatsUpdate(flow);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="live-feed">
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 20,
      }}>
        <div>
          <div style={{ fontSize: 10, color: "#7C8CA5", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 4 }}>
            Live Threat Feed
          </div>
          <div style={{ fontSize: 11, color: "#54514b" }}>
            {flows.length} flows · threats stay · benign fades
          </div>
        </div>
      </div>

      <div style={{ overflowY: "auto", maxHeight: "calc(100vh - 280px)" }}>
        {flows.length === 0 ? (
          <div style={{ color: "#1F2937", textAlign: "center", padding: "60px 0", fontSize: 13 }}>
            Waiting for traffic...
          </div>
        ) : (
          flows.map(flow => (
            <FlowCard
              key={flow.id}
              flow={flow}
            />
          ))
        )}
      </div>
    </div>
  );
}