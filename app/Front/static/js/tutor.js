document.addEventListener("DOMContentLoaded", () => {

    const btnGenerate = document.getElementById("btnGenerate");
    const btnCheck = document.getElementById("btnCheck");

    const exerciseBox = document.getElementById("exerciseBox");
    const exerciseText = document.getElementById("exerciseText");
    const userAnswer = document.getElementById("userAnswer");

    const feedbackBox = document.getElementById("feedbackBox");
    const feedbackText = document.getElementById("feedbackText");

    let currentExerciseId = null;

    // Generar ejercicio
    btnGenerate.addEventListener("click", async () => {
        const res = await fetch("/api/tutor/question", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        const data = await res.json();

        currentExerciseId = data.id;
        exerciseText.textContent = data.exercise;
        exerciseBox.classList.remove("hidden");
        feedbackBox.classList.add("hidden");
    });

    // Verificar respuesta del usuario
    btnCheck.addEventListener("click", async () => {

        if (!userAnswer.value) return;

        const res = await fetch("/api/tutor/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                id: currentExerciseId,
                answer: userAnswer.value
            })
        });

        const data = await res.json();

        feedbackText.textContent = data.correct
            ? "¡Correcto! ✔️ " + data.explanation
            : "Incorrecto ✖️ " + data.explanation;

        feedbackText.className =
            data.correct
                ? "text-green-600 text-lg"
                : "text-red-600 text-lg";

        feedbackBox.classList.remove("hidden");
    });
});
