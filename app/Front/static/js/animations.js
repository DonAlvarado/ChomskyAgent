document.addEventListener("DOMContentLoaded", () => {

    // 1. Animación inicial del body
    document.body.classList.add("ca-anim-fade-in");

    // 2. Animar elementos marcados con data-anim en scroll
    const animatedElems = document.querySelectorAll("[data-anim]");
    if (animatedElems.length === 0) return;

    const options = {
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;

            const el = entry.target;
            const type = el.getAttribute("data-anim");

            el.classList.remove("ca-anim-hidden");

            switch (type) {
                case "fade":
                    el.classList.add("ca-anim-fade-in");
                    break;
                case "slide-up":
                    el.classList.add("ca-anim-slide-up");
                    break;
                case "scale":
                    el.classList.add("ca-anim-scale-in");
                    break;
                default:
                    el.classList.add("ca-anim-fade-in");
            }

            observer.unobserve(el);
        });
    }, options);

    animatedElems.forEach(el => {
        // asegurar estado inicial
        el.classList.add("ca-anim-hidden");
        observer.observe(el);
    });
});
