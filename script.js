function openChat() {
  document.getElementById("chatbox").classList.remove("hidden");
  document.getElementById("gemini-icon").style.display = "none";

  // Auto-focus on input
  setTimeout(() => {
    document.getElementById("user-input").focus();
  }, 100);
}

function closeChat() {
  document.getElementById("chatbox").classList.add("hidden");
  document.getElementById("gemini-icon").style.display = "flex";
}

async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value;
  if (!message.trim()) return;

  appendMessage("You", message);
  input.value = "";

  const res = await fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  const data = await res.json();
  appendMessage("Bot", data.reply);
}

function appendMessage(sender, text) {
  const chatLog = document.getElementById("chat-log");

  const wrapper = document.createElement("div"); // Wrapper to control alignment
  const msg = document.createElement("div");

  if (sender === "You") {
    msg.className = "user-msg";
  } else {
    msg.className = "bot-msg";
  }

  msg.textContent = text;
  wrapper.appendChild(msg);
  chatLog.appendChild(wrapper);
  chatLog.scrollTop = chatLog.scrollHeight;
}



// ✅ Add this to enable Enter key to send message
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("user-input");
  input.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault(); // Prevents line break
      sendMessage();          // Call send message
    }
  });
});