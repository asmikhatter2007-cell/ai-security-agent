import { useState, useEffect, useRef } from "react";

function AnimatedNumber({ target }) {
  const [display, setDisplay] = useState(target);
  const prevRef = useRef(target);
  const [flash, setFlash] = useState(false);

  useEffect(() => {
    if (target !== prevRef.current) {
      setFlash(true);
      setTimeout(() => setFlash(false), 400);
      prevRef.current = target;
      setDisplay(target);
    }
  }, [target]);

  return (
    <span style={{
      display: "inline-block",
      transform: flash ? "scale(1.15)" : "scale(1)",
      transition: "transform 0.2s ease",
    }}>
      {display}
    </span>
  );
}

const STAT_CONFIG = [
  { label: "Flows Processed", key: "total", color: "#60A5FA" },
  { label: "Threats Detected", key: "threats", color: "#EF4444" },
  { label: "Benign", key: "benign", color: "#10B981" },
  { label: "Threat Rate", key: "rate", color: "#F59E0B", suffix: "%" },
];

export default function StatCards({ data = { total: 0, threats: 0, benign: 0 } }) {
  const rate = data.total > 0
    ? ((data.threats / data.total) * 100).toFixed(1)
    : "0.0";

  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(4, 1fr)",
      gap: 16,
      padding: "0 30px 30px",
    }}>
      {STAT_CONFIG.map(({ label, key, color, suffix }) => (
        <div key={key} style={{
          background: "#0D1B2E",
          border: "1px solid #1E3A5F",
          borderRadius: 16,
          padding: "20px 24px",
          position: "relative",
          overflow: "hidden",
        }}>
          {/* Subtle top accent line */}
          <div style={{
            position: "absolute",
            top: 0, left: 0, right: 0,
            height: 2,
            background: `linear-gradient(90deg, transparent, ${color}60, transparent)`,
          }} />

          <div style={{
            fontSize: 10,
            color: "#334155",
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            marginBottom: 12,
          }}>
            {label}
          </div>

          <div style={{
            fontSize: 36,
            fontWeight: 700,
            color,
            fontFamily: "'JetBrains Mono', monospace",
            letterSpacing: "-0.02em",
          }}>
            <AnimatedNumber target={key === "rate" ? rate : data[key]} />
            {suffix}
          </div>
        </div>
      ))}
    </div>
  );
}