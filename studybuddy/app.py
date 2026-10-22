from flask import Flask, render_template, request, jsonify
from buddy import get_reply

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    history = data.get("history") or []
    if not message:
        return jsonify({"error": "Type a message first."}), 400
    return jsonify({"reply": get_reply(message, history)})


if __name__ == "__main__":
    app.run(debug=True)
