const STUDENT_ID = "Filonenko";
const API_BASE = "http://127.0.0.1:8000";

let chart = null;

document.getElementById("analyze-btn").addEventListener("click", async () => {
  await fetch(`${API_BASE}/fetch/${STUDENT_ID}`, { method: "POST" });
  await fetch(`${API_BASE}/analyze/${STUDENT_ID}`, { method: "POST" });
  loadSentimentChart();
});

async function loadSentimentChart() {
  const res = await fetch(`${API_BASE}/sentiment/${STUDENT_ID}`);
  const data = await res.json();

  const ctx = document.getElementById("sentimentChart").getContext("2d");

  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Позитивні", "Нейтральні", "Негативні"],
      datasets: [{
        label: "Кількість новин",
        data: [data.positive, data.neutral, data.negative],
        backgroundColor: ["#4caf50", "#ffeb3b", "#f44336"]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: "Тональність новин" }
      }
    }
  });
}
