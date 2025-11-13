document.addEventListener("DOMContentLoaded", () => {
    const chatWindow = document.getElementById("chatWindow");
    const chatInput = document.getElementById("chatInput");
    const btnSend = document.getElementById("btnSend");

    function appendMessage(text, sender) {
        const div = document.createElement("div");
        div.className =
            sender === "user"
                ? "bg-turquoise text-white p-3 rounded-lg w-fit ml-auto"
                : "bg-gray-200 text-gray-800 p-3 rounded-lg w-fit";

        div.textContent = text;
        chatWindow.appendChild(div);

        chatWindow.scrollTo(0, chatWindow.scrollHeight);
    }

    btnSend.addEventListener("click", async () => {

        const msg = chatInput.value.trim();
        if (!msg) return;

        appendMessage(msg, "user");
        chatInput.value = "";

        const res = await fetch("/api/agent/message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });

        const data = await res.json();

        appendMessage(data.reply, "ai");
    });

    // Enter para enviar
    chatInput.addEventListener("keypress", e => {
        if (e.key === "Enter") btnSend.click();
    });
});
