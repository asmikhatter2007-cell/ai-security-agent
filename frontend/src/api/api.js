const BASE_URL = "http://127.0.0.1:8000";

export async function predictFlow(features) {
    const response = await fetch(`${BASE_URL}/predict`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            features,
        }),
    });

    if (!response.ok) {
        throw new Error("Prediction failed");
    }

    return await response.json();
}