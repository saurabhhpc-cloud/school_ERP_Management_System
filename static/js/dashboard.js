document.addEventListener("DOMContentLoaded", function () {

  // Data injected from Django (global vars)
  const monthlyLabels = window.MONTH_LABELS || [];
  const monthlyValues = window.MONTH_VALUES || [];

  const paidAmount = window.PAID_AMOUNT || 0;
  const pendingAmount = window.PENDING_AMOUNT || 0;

  // Monthly Fees (Bar)
  const feesCtx = document.getElementById("monthlyFeesChart");
  if (feesCtx) {
    new Chart(feesCtx, {
      type: "bar",
      data: {
        labels: monthlyLabels,
        datasets: [{
          label: "Fees Collected (₹)",
          data: monthlyValues,
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
      }
    });
  }

  // Paid vs Pending (Donut)
  const statusCtx = document.getElementById("statusChart");
  if (statusCtx) {
    new Chart(statusCtx, {
      type: "doughnut",
      data: {
        labels: ["Paid", "Pending"],
        datasets: [{
          data: [paidAmount, pendingAmount]
        }]
      },
      options: { responsive: true }
    });
  }
});
document.addEventListener("DOMContentLoaded", function () {
borderColor: getComputedStyle(document.documentElement)
              .getPropertyValue('--brand-primary')
    // =========================
    // Monthly Fee Chart
    // =========================
    const feeCtx = document.getElementById("monthlyFeeChart");

    if (feeCtx) {
        new Chart(feeCtx, {
            type: "line",
            data: {
                labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                datasets: [{
                    data: [420000,390000,450000,480000,500000,470000,520000,560000,540000,580000,600000,650000],
                    borderColor: "#4f46e5",
                    backgroundColor: "rgba(79,70,229,0.1)",
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

});
