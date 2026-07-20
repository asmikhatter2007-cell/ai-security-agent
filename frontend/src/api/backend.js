const BASE_URL="http://127.0.0.1:8000";

export async function getNextFlow(){
    const response=await fetch(`${BASE_URL}/next-flow`);

    if(!response.ok){
        throw new Error("Backend unavailable");
    }

    return await response.json();
}

export async function generateReport(flow) {

  const response = await fetch(`${BASE_URL}/generate-report`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      agent1_summary: flow.agent1_summary,
      current_flow: flow.current_flow,
      agent2_result: flow.agent2_result,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to generate report");
  }

  return await response.json();
}