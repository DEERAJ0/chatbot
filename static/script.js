async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;

    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `
        <div class='message user'>
            <div class='message-content'>${message}</div>
        </div>
    `;

    input.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });
        const data = await response.json();
        chatBox.innerHTML += `
            <div class='message bot'>
                <div class='message-content'>${data.response}</div>
            </div>
        `;
    } catch (error) {
        chatBox.innerHTML += `
            <div class='message bot'>
                <div class='message-content'>Error: ${error.message}</div>
            </div>
        `;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}
