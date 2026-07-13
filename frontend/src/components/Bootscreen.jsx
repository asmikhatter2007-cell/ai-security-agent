import { useState, useEffect } from "react";

const BOOT_STEPS = [
  "Initializing AI Security Agent...",
  "Loading Random Forest model...",
  "Connecting to Qwen 2.5 LLM...",
  "Calibrating threat detection thresholds...",
  "Starting live network monitor...",
  "System ready.",
];

export default function BootScreen({ onComplete }) {
  const [step, setStep] = useState(0);
  const [done, setDone] = useState(false);
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    if (step < BOOT_STEPS.length - 1) {
      const t = setTimeout(() => setStep(s => s + 1), 550);
      return () => clearTimeout(t);
    } else {
      const t1 = setTimeout(() => setFadeOut(true), 800);
      const t2 = setTimeout(() => onComplete(), 1500);
      return () => { clearTimeout(t1); clearTimeout(t2); };
    }
  }, [step]);

  return (
    <div style={{
      position: "fixed",
      inset: 0,
      background: "#060E1A",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 9999,
      opacity: fadeOut ? 0 : 1,
      transition: "opacity 0.6s ease",
    }}>
      {/* Logo */}
      <div style={{
        width: 64,
        height: 64,
        borderRadius: 16,
        background: "linear-gradient(135deg, #1D4ED8, #0EA5E9)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: 32,
        marginBottom: 32,
        boxShadow: "0 0 35px rgba(14,165,233,0.35), 0 0 70px rgba(29,78,216,0.15)",
      }}>
        🛡️
      </div>

      <div style={{
        fontSize: 22,
        fontWeight: 700,
        color: "#E2E8F0",
        letterSpacing: "0.08em",
        marginBottom: 8,
      }}>
        AI SECURITY AGENT
      </div>

      <div style={{
        fontSize: 11,
        color: "#334155",
        letterSpacing: "0.12em",
        marginBottom: 48,
        textTransform: "uppercase",
      }}>
        Network Intrusion Detection System
      </div>

      {/* Boot log */}
      <div style={{
        width: 360,
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 12,
      }}>
        {BOOT_STEPS.slice(0, step + 1).map((s, i) => (
          <div key={i} style={{
            color: i === step ? "#38BDF8" : "#1E3A5F",
            textshadow:"0 0 10px rgba(56,189,248,0.6)",
            marginBottom: 6,
            transition: "color 1s ease",
          }}>
            <span style={{ color: i === step ? "#0EA5E9" : "#1E3A5F", marginRight: 8 }}>
              {i < step ? "✓" : i === step ? "›" : " "}
            </span>
            {s}
          </div>
        ))}
      </div>

      {/* Progress bar */}
      <div style={{
        width: 360,
        height: 2,
        background: "#0D1B2E",
        borderRadius: 1,
        marginTop: 24,
        overflow: "hidden",
      }}>
        <div style={{
          height: "100%",
          width: `${((step + 1) / BOOT_STEPS.length) * 100}%`,
          background: "linear-gradient(90deg, #2563EB, #0EA5E9)",
          boxShadow:"0 0 12px rgba(14,165,233,0.5)",
          transition: "width 1s ease",
        }} />
      </div>
    </div>
  );
}