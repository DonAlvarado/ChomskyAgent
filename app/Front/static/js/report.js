document.addEventListener("DOMContentLoaded", () => {

    const btnLoad = document.getElementById("btnLoadReports");
    const list = document.getElementById("reportList");

    btnLoad.addEventListener("click", async () => {

        const res = await fetch("/api/report/list", {
            method: "GET"
        });

        const data = await res.json();

        list.innerHTML = "";

        data.reports.forEach(rep => {
            const li = document.createElement("li");
            li.className = "p-4 bg-gray-100 rounded-lg flex justify-between items-center";

            li.innerHTML = `
                <span class="text-gray-700">
                    <strong>${rep.id}</strong> — ${rep.timestamp}
                </span>

                <a href="${rep.file_url}" 
                   class="px-4 py-2 bg-turquoise text-white rounded-lg hover:bg-cyanlight transition">
                    Descargar
                </a>
            `;

            list.appendChild(li);
        });
    });
});
