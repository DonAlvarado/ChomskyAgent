document.addEventListener("DOMContentLoaded", () => {

    const btnAnalyze = document.getElementById("btnAnalyzeAutomaton");
    const btnDiagram = document.getElementById("btnAutomatonDiagram");
    const input = document.getElementById("automatonInput");

    const outBox = document.getElementById("automatonOutput");
    const typeBox = document.getElementById("automatonType");
    const explainBox = document.getElementById("automatonExplain");

    const diagramBox = document.getElementById("automatonDiagram");
    const svgContainer = document.getElementById("automatonSvgContainer");

    if (!btnAnalyze || !input) return;

    let lastPayload = null;

    // Analizar autómata
    btnAnalyze.addEventListener("click", async () => {
        const raw = input.value.trim();
        if (!raw) return;

        let obj;
        try {
            obj = JSON.parse(raw);
        } catch {
            typeBox.textContent = "Error: JSON inválido.";
            explainBox.innerHTML = "";
            outBox.classList.remove("hidden");
            return;
        }

        lastPayload = obj;

        const res = await fetch("/api/automata/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(obj)
        });

        const data = await res.json();

        if (!data.success) {
            typeBox.textContent = "Error: " + (data.error || "No se pudo analizar el autómata.");
            explainBox.innerHTML = "";
            outBox.classList.remove("hidden");
            return;
        }

        typeBox.textContent = "Tipo detectado: " + data.type;

        explainBox.innerHTML = "";
        if (data.type === "AFD") {
            const li = document.createElement("li");
            li.textContent = "Transiciones deterministas.";
            explainBox.appendChild(li);
        } else if (data.type === "AFN") {
            const li = document.createElement("li");
            li.textContent = "Transiciones múltiples por símbolo.";
            explainBox.appendChild(li);
        } else if (data.type === "AFN-ε") {
            const li = document.createElement("li");
            li.textContent = "El autómata contiene transiciones ε.";
            explainBox.appendChild(li);
        }

        outBox.classList.remove("hidden");
    });

    // Visualizar diagrama
    if (btnDiagram) {
        btnDiagram.addEventListener("click", async () => {
            const raw = input.value.trim();
            if (!raw && !lastPayload) return;

            let payload = lastPayload;
            if (!payload) {
                try {
                    payload = JSON.parse(raw);
                } catch {
                    typeBox.textContent = "Error: JSON inválido.";
                    explainBox.innerHTML = "";
                    outBox.classList.remove("hidden");
                    return;
                }
            }

            const res = await fetch("/api/automata/visualize", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await res.json();

            if (!data.success) {
                svgContainer.innerHTML = "<p class='text-red-600'>No se pudo generar el diagrama.</p>";
                diagramBox.classList.remove("hidden");
                return;
            }

            svgContainer.innerHTML = data.svg;
            diagramBox.classList.remove("hidden");
        });
    }
});
