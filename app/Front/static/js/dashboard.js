document.addEventListener("DOMContentLoaded", () => {
    const dashboardRoot = document.querySelector("[data-page='dashboard']");
    if (!dashboardRoot) return; // Solo corre en dashboard

    const cards = dashboardRoot.querySelectorAll("[data-dashboard-card]");

    cards.forEach(card => {
        card.classList.add("ca-card-hover", "ca-anim-hidden");

        card.addEventListener("click", () => {
            cards.forEach(c => c.classList.remove("ring-2", "ring-turquoise"));
            card.classList.add("ring-2", "ring-turquoise");
        });
    });

    // Animación de entrada secuencial
    let delay = 0;
    cards.forEach(card => {
        setTimeout(() => {
            card.classList.remove("ca-anim-hidden");
            card.classList.add("ca-anim-slide-up");
        }, delay);
        delay += 80;
    });
});
