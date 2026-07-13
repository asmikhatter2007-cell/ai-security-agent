const agents = [
  {
    name: "Agent 1",
    role: "Random Forest",
    color: "#0EA5E9",
    latency: "8ms",
    processed: 0,
  },
  {
    name: "Agent 2",
    role: "Qwen 2.5 LLM",
    color: "#A855F7",
    latency: "1.2s",
    processed: 0,
  },
  {
    name: "Agent 3",
    role: "Report Formatter",
    color: "#10B981",
    latency: "2ms",
    processed: 0,
  },
];

function Sidebar({ active = null }) {
  return (
    <div className="sidebar">
      <div
        style={{
          fontSize: 10,
          color: "#7C8CA5",
          letterSpacing: "0.1em",
          textTransform: "uppercase",
          marginBottom: 20,
        }}
      >
        Agent Pipeline
      </div>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 12,
        }}
      >
        {agents.map((agent, i) => (
          <div
            key={i}
            style={{
              background: "#0D1117",
              border: `1px solid ${
                active === i ? agent.color : "rgba(255,255,255,0.05)"
              }`,
              borderRadius: 12,
              padding: "14px 16px",
              boxShadow:
                active === i
                  ? `0 0 16px ${agent.color}30`
                  : "none",
              transition: "all 0.3s ease",
            }}
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                marginBottom: 8,
              }}
            >
              <div
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background:
                    active === i ? agent.color : "#1F2937",
                  boxShadow:
                    active === i
                      ? `0 0 8px ${agent.color}`
                      : "none",
                  transition: "all 0.3s ease",
                }}
              />

              <span
                style={{
                  color: "#E5E7EB",
                  fontSize: 13,
                  fontWeight: 600,
                }}
              >
                {agent.name}
              </span>

              <span
                style={{
                  marginLeft: "auto",
                  fontSize: 10,
                  color: "#10B981",
                  fontWeight: 600,
                  letterSpacing: "0.06em",
                }}
              >
                READY
              </span>
            </div>

            <div style={{ paddingLeft: 16 }}>
              <div
                style={{
                  color: "#7C8CA5",
                  fontSize: 11,
                  marginBottom: 6,
                }}
              >
                {agent.role}
              </div>

              <div
                style={{
                  display: "flex",
                  gap: 16,
                }}
              >
                <div>
                  <div
                    style={{
                      color: "#7C8CA5",
                      fontSize: 10,
                    }}
                  >
                    Latency
                  </div>

                  <div
                    style={{
                      color: agent.color,
                      fontSize: 12,
                      fontFamily: "'JetBrains Mono', monospace",
                      fontWeight: 600,
                    }}
                  >
                    {agent.latency}
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Sidebar;