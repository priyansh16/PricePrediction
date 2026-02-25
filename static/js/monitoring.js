let usageChart;
let avgChart;
let municipalityChart;

function loadDashboard() {

    const startDate = document.getElementById("startDate")?.value;
    const endDate = document.getElementById("endDate")?.value;

    let url = "/monitoring-data";

    if (startDate && endDate) {
        url += `?start=${startDate}&end=${endDate}`;
    }

    fetch(url)
    .then(response => response.json())
    .then(data => {

        if (!data.usage_dates) return;

        // Usage Chart
        if (usageChart) usageChart.destroy();

        usageChart = new Chart(document.getElementById("usageChart"), {
            type: "line",
            data: {
                labels: data.usage_dates,
                datasets: [{
                    label: "Prediction Count Per Day",
                    data: data.usage_counts,
                    borderColor: "#2ecc71",
                    backgroundColor: "rgba(46, 204, 113, 0.3)",
                    fill: true,
                    tension: 0.3
                }]
            }
        });

        // Average Chart
        if (avgChart) avgChart.destroy();

        let datasets = [];
        const colors = ["#9b59b6", "#e67e22", "#3498db", "#2ecc71", "#e74c3c", "#f1c40f"];
        let colorIndex = 0;

        for (const [houseType, values] of Object.entries(data.avg_values)) {
            datasets.push({
                label: houseType,
                data: values,
                borderColor: colors[colorIndex % colors.length],
                fill: false,
                tension: 0.3
            });
            colorIndex++;
        }

        avgChart = new Chart(document.getElementById("avgPriceChart"), {
            type: "line",
            data: {
                labels: data.avg_dates,
                datasets: datasets
            }
        });

        // Municipality Chart
        if (municipalityChart) municipalityChart.destroy();

        municipalityChart = new Chart(document.getElementById("municipalityChart"), {
            type: "bar",
            data: {
                labels: data.municipalities,
                datasets: [{
                    label: "Predictions per Municipality",
                    data: data.municipality_counts,
                    backgroundColor: ["#3498db", "#e67e22", "#e74c3c", "#1abc9c", "#f1c40f"]
                }]
            }
        });

        // Table
        const tableBody = document.querySelector("#logsTable tbody");
        tableBody.innerHTML = "";

        data.recent_logs.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${row.Municipality}</td>
                <td>${row.Living_area}</td>
                <td>${row.Prediction}</td>
                <td>${row.Timestamp}</td>
            `;
            tableBody.appendChild(tr);
        });

    });
}

// Auto load when page ready
document.addEventListener("DOMContentLoaded", function () {
    loadDashboard();

setInterval(() => {
        console.log("Auto refreshing dashboard...");
        loadDashboard();
    }, 60000);
});