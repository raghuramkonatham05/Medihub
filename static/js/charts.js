const ctx = document.getElementById("hba1cChart");

new Chart(ctx, {
  type: "line",
  data: {
    labels: ["Jan", "Feb", "Mar", "Apr", "May"],
    datasets: [{
      label: "HbA1c",
      data: [6.2, 6.5, 6.8, 7.0, 7.2],
      borderColor: "#ef4444",
      tension: 0.4,
      fill: false
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false }
    }
  }
});
