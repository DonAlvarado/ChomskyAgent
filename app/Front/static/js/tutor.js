document.addEventListener("DOMContentLoaded", () => {

    const btnGenerate = document.getElementById("btnGenerate");
    const btnCheck = document.getElementById("btnCheck");

    const exerciseBox = document.getElementById("exerciseBox");
    const exerciseText = document.getElementById("exerciseText");
    const userAnswer = document.getElementById("userAnswer");

    const feedbackBox = document.getElementById("feedbackBox");
    const feedbackText = document.getElementById("feedbackText");

    let currentExerciseId = null;
    let currentQuestion = null;
    let currentType = null;

    // Generar ejercicio
    btnGenerate.addEventListener("click", async () => {
        const res = await fetch("/api/tutor/question", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ difficulty: "basic" })
        });

        const data = await res.json();
        if (!data.success) {
            feedbackText.textContent = data.error || "No se pudo generar el ejercicio.";
            feedbackText.className = "text-red-600 text-lg";
            feedbackBox.classList.remove("hidden");
            return;
        }

        currentExerciseId = data.id;
        currentQuestion = data.question;
        currentType = data.type;

        // Mostrar la gramática en formato texto
        const productions = data.question;
        let text = "";
        for (const A in productions) {
            if (!Object.prototype.hasOwnProperty.call(productions, A)) continue;
            text += `${A} -> ${productions[A].join(" | ")}\n`;
        }
        exerciseText.textContent = text.trim();

        exerciseBox.classList.remove("hidden");
        feedbackBox.classList.add("hidden");
    });

    // Verificar respuesta del usuario
    btnCheck.addEventListener("click", async () => {
        if (!userAnswer.value.trim()) return;
        if (!currentQuestion || !currentType) return;

        const res = await fetch("/api/tutor/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                id: currentExerciseId,
                type: currentType,
                question: currentQuestion,
                answer: userAnswer.value.trim()
            })
        });

        const data = await res.json();
        if (!data.success) {
            feedbackText.textContent = data.error || "No se pudo verificar la respuesta.";
            feedbackText.className = "text-red-600 text-lg";
            feedbackBox.classList.remove("hidden");
            return;
        }

        feedbackText.textContent = data.correct
            ? `¡Correcto! ✔️ La gramática es ${data.correct_type}.`
            : `Incorrecto ✖️ El tipo correcto es ${data.correct_type}.`;

        feedbackText.className = data.correct
            ? "text-green-600 text-lg"
            : "text-red-600 text-lg";

        feedbackBox.classList.remove("hidden");
    });
});
