document.addEventListener("DOMContentLoaded", () => {

    const btnLoad = document.getElementById("btnLoadReports");
    const list = document.getElementById("reportList");

    if (!btnLoad || !list) return;

    btnLoad.addEventListener("click", async () => {
        const res = await fetch("/api/report/list", {
            method: "GET"
        });

        const data = await res.json();

        list.innerHTML = "";

        const reports = data.reports || [];

        reports.forEach(fileName => {
            const li = document.createElement("li");
            li.className = "p-4 bg-gray-100 rounded-lg flex justify-between items-center";

            li.innerHTML = `
                <span class="text-gray-700">
                    <strong>${fileName}</strong>
                </span>

                <a href="/static/generated/${fileName}"
                   class="px-4 py-2 bg-turquoise text-white rounded-lg hover:bg-cyanlight transition"
                   target="_blank" rel="noopener noreferrer">
                    Descargar
                </a>
            `;

            list.appendChild(li);
        });
    });
});
