const chat = document.getElementById("chat");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const history = [];

function addMessage(text, who) {
  const div = document.createElement("div");
  div.className = "msg " + who;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

async function send(text) {
  text = text.trim();
  if (!text) return;
  addMessage(text, "user");
  input.value = "";
  const typing = addMessage("Sage is thinking...", "buddy typing");
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history }),
    });
    const data = await res.json();
    typing.remove();
    const reply = data.reply || data.error || "Something went wrong. Try again.";
    addMessage(reply, "buddy");
    history.push({ role: "user", content: text }, { role: "assistant", content: reply });
  } catch (err) {
    typing.remove();
    addMessage("I can't reach the server. Is it still running?", "buddy");
  }
}

sendBtn.addEventListener("click", () => send(input.value));
input.addEventListener("keydown", (e) => { if (e.key === "Enter") send(input.value); });
document.querySelectorAll(".chip").forEach((c) =>
  c.addEventListener("click", () => send(c.dataset.text))
);
