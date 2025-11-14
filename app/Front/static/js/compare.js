document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("compare-btn");
    const rDiv = document.getElementById("compare-result");
    const g1El = document.getElementById("g1");
    const g2El = document.getElementById("g2");

    if (!btn || !rDiv || !g1El || !g2El) return;

    btn.addEventListener("click", () => {
        const g1 = g1El.value
            .split("\n")
            .map(r => r.trim())
            .filter(r => r.length > 0);

        const g2 = g2El.value
            .split("\n")
            .map(r => r.trim())
            .filter(r => r.length > 0);

        if (g1.length === 0 || g2.length === 0) {
            rDiv.textContent = "Ingresa ambas gramáticas antes de comparar.";
            return;
        }

        rDiv.textContent = "Comparando...";

        fetch("/api/compare/grammars", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ g1, g2 })
        })
        .then(res => res.json())
        .then(data => {
            if (!data.success) {
                rDiv.textContent = data.error || "Error al comparar gramáticas.";
                return;
            }

            const r = data.result;
            let html = "";

            // Encabezado equivalencia
            if (r.equivalent) {
                html += `<p class="text-green-700 font-semibold">✔ Las gramáticas parecen equivalentes.</p>`;
            } else {
                html += `<p class="text-red-700 font-semibold">✘ Las gramáticas NO son equivalentes.</p>`;
            }

            // Lenguajes
            html += `<div class="mt-3 text-sm">`;
            html += `<p><b>L(G1) ≤ ${r.max_len}:</b> ${JSON.stringify(r.L1)}</p>`;
            html += `<p><b>L(G2) ≤ ${r.max_len}:</b> ${JSON.stringify(r.L2)}</p>`;

            // Diferencias si existen
            if (!r.equivalent) {
                html += `<p class="mt-2"><b>L1 - L2:</b> ${JSON.stringify(r.L1_minus_L2)}</p>`;
                html += `<p><b>L2 - L1:</b> ${JSON.stringify(r.L2_minus_L1)}</p>`;
            }

            html += `</div>`;

            rDiv.innerHTML = html;
        })

        .catch(() => {
            rDiv.textContent = "No se pudo contactar a /api/compare/grammars.";
        });
    });
});
