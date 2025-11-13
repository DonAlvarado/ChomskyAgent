document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("regexInput");
    const outBox = document.getElementById("convOutput");
    const result = document.getElementById("convResult");

    // Mostrar texto formateado en el output
    function show(text) {
        result.textContent = text;
        outBox.classList.remove("hidden");
    }

    // Llamada genérica a los endpoints del converter
    async function callEndpoint(path) {
        const regex = input.value.trim();
        if (!regex) return alert("Ingresa una expresión regular.");

        const res = await fetch(`/api/converter/${path}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ regex })
        });

        const data = await res.json();

        if (!data.success) {
            show("Error: " + (data.error || "No se pudo convertir la expresión."));
        } else {
            show(JSON.stringify(data, null, 2));
        }
    }

    // Botones
    document.getElementById("btnRegexToNFA").addEventListener("click", () => {
        callEndpoint("regex2nfa");
    });

    document.getElementById("btnRegexToAFD").addEventListener("click", () => {
        callEndpoint("regex2afd");
    });

    document.getElementById("btnRegexToGrammar").addEventListener("click", () => {
        callEndpoint("regex2grammar");
    });

    document.getElementById("btnRegexToAFDMin").addEventListener("click", () => {
        callEndpoint("regex2afd_min");
    });

    document.getElementById("btnVisualizeAFDMin").addEventListener("click", async () => {
    const txt = document.getElementById("convResult").textContent.trim();
    if (!txt) return alert("Primero genera el AFD minimizado.");

    const json = JSON.parse(txt);
    if (!json.afd_min) return alert("El resultado actual no es un AFD minimizado.");

    const res = await fetch("/api/automata/visualize_min", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ afd_min: json.afd_min })
    });

    const data = await res.json();
    if (!data.success) return alert("No se pudo visualizar el AFD minimizado.");
        show(data.svg);
    });

});
