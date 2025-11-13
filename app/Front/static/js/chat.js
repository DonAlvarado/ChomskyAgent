document.addEventListener("DOMContentLoaded", () => {
    const chatWindow = document.getElementById("chatWindow");
    const chatInput = document.getElementById("chatInput");
    const btnSend = document.getElementById("btnSend");

    function appendMessage(text, sender) {
        const div = document.createElement("div");
        div.className =
            sender === "user"
                ? "bg-turquoise text-white p-3 rounded-lg w-fit ml-auto my-1"
                : "bg-gray-200 text-gray-800 p-3 rounded-lg w-fit my-1";

        div.textContent = text;
        chatWindow.appendChild(div);

        chatWindow.scrollTo(0, chatWindow.scrollHeight);
    }

    async function sendMessage() {
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

        const reply = data.reply;
        const textToShow =
            typeof reply === "string"
                ? reply
                : JSON.stringify(reply, null, 2);

        appendMessage(textToShow, "ai");
    }

    btnSend.addEventListener("click", sendMessage);

    chatInput.addEventListener("keypress", e => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });
});
