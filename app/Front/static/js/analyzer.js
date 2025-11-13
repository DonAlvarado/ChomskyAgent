document.addEventListener("DOMContentLoaded", () => {

    const btn = document.getElementById("btnAnalyze");
    const input = document.getElementById("grammarInput");
    const box = document.getElementById("analysisOutput");
    const type = document.getElementById("resultType");
    const explain = document.getElementById("resultExplain");

    btn.addEventListener("click", async () => {

        const text = input.value.trim();
        if (!text) return;

        const res = await fetch("/api/grammar/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ rules: text })
        });

        const data = await res.json();

        type.textContent = "Tipo detectado: " + data.type;
        explain.innerHTML = "";

        data.explanation.forEach(step => {
            const li = document.createElement("li");
            li.textContent = step;
            explain.appendChild(li);
        });

        box.classList.remove("hidden");
    });
});
