document.addEventListener("DOMContentLoaded", () => {

    const btn = document.getElementById("btnAnalyze");
    const input = document.getElementById("grammarInput");
    const box = document.getElementById("analysisOutput");
    const type = document.getElementById("resultType");
    const explain = document.getElementById("resultExplain");

    btn.addEventListener("click", async () => {
        const text = input.value.trim();
        if (!text) return;

        // Convertir el textarea en lista de reglas
        const rules = text
            .split("\n")
            .map(r => r.trim())
            .filter(r => r.length > 0);

        const res = await fetch("/api/grammar/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ rules })
        });

        const data = await res.json();
        if (!data.success) {
            type.textContent = "Error: " + (data.error || "No se pudo analizar la gramática.");
            explain.innerHTML = "";
            box.classList.remove("hidden");
            return;
        }

        type.textContent = "Tipo detectado: " + data.classification.type;

        explain.innerHTML = "";
        data.classification.steps.forEach(step => {
            const li = document.createElement("li");
            li.textContent = step;
            explain.appendChild(li);
        });

        box.classList.remove("hidden");
    });
});
