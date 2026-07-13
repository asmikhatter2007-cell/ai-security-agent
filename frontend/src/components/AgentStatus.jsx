function AgentStatus() {
  const agents = [
    { name: "Agent 1", role: "Random Forest", status: "Ready" },
    { name: "Agent 2", role: "LLM Behaviour", status: "Ready" },
    { name: "Agent 3", role: "SOC Summary", status: "Ready" },
  ];

  return (
    <section className="agent-section">
      <h3>Agent Status</h3>

      <div className="agent-grid">
        {agents.map((agent, index) => (
          <div className="agent-card" key={index}>
            <div className="status-dot"></div>

            <h4>{agent.name}</h4>

            <p>{agent.role}</p>

            <span>{agent.status}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

export default AgentStatus;