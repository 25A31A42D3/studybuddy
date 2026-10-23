"""The study buddy's brain.

If GEMINI_API_KEY is set (in the .env file), Sage answers using the Gemini API.
If not, she falls back to a few simple built-in replies so the app still runs.
"""
import os

from dotenv import load_dotenv

load_dotenv()

PERSONALITY = """You are Sage, a warm, calm study buddy for people who find it
hard to study around others (introverts). You are a friend, not a strict teacher.

Style:
- Keep replies short: 2-4 sentences. Use simple words.
- Teach in small steps. Ask only ONE question at a time.
- Never judge mistakes. Celebrate small wins.
- If the person seems stuck or tired, encourage them gently and shrink the task.

When the person asks for a quiz:
- If they gave a topic, ask question 1 right away. Do not ask what they want.
- Ask ONE question, then wait for their answer.
- After they answer, say if it is right or wrong, explain kindly in 1-2 sentences,
  then ask the next question. Do a short quiz of 5 questions, easy to harder.
- At the end, give a score and one encouraging sentence.

When the person asks to study a topic:
- Explain the first small idea with one simple example, then ask one check question.

When the person has a doubt:
- Answer it clearly in simple words, with a tiny example, then ask if it makes sense."""

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
_client = None


def _get_client():
    global _client
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=key)
    return _client


def fallback_reply(message):
    text = message.lower()
    if any(w in text for w in ("hi", "hello", "hey")):
        return "Hey, glad you're here. What are we studying today? We can take it slow."
    if "quiz" in text:
        return "Sure, let's do a quick one. Tell me the topic and I'll start easy."
    if any(w in text for w in ("tired", "stuck", "can't", "cant")):
        return "That's okay. Let's shrink the task: just one small piece for five minutes. Which part feels hardest?"
    return "I'm with you. Tell me what you're working on and we'll go through it together."


def get_reply(message, history):
    client = _get_client()
    if client is None:
        return fallback_reply(message)

    from google.genai import types

    contents = []
    for turn in history[-12:]:
        role = "user" if turn.get("role") == "user" else "model"
        contents.append(
            types.Content(role=role, parts=[types.Part(text=turn.get("content", ""))])
        )
    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=PERSONALITY,
                max_output_tokens=800,
            ),
        )
        return (response.text or "").strip() or fallback_reply(message)
    except Exception as err:
        print("LLM error:", err)
        return f"DEBUG ERROR: {err}"