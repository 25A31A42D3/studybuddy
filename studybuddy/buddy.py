"""The study buddy's brain.

Day 1: simple built-in replies so the app runs with no API key.
Day 1 (next step): replace get_reply() with a call to an LLM,
using PERSONALITY as the system prompt.
"""

PERSONALITY = """You are Sage, a warm, calm study buddy for people who find it
hard to study around others (introverts). You are a friend, not a strict teacher.
Keep replies short (2-4 sentences). Teach in small steps, ask one question at a
time, never judge mistakes, and celebrate small wins. If the person seems stuck
or tired, encourage them gently."""


def get_reply(message, history):
    text = message.lower()
    if any(w in text for w in ("hi", "hello", "hey")):
        return "Hey, glad you're here. What are we studying today? We can take it slow."
    if "quiz" in text:
        return "Sure, let's do a quick one. Tell me the topic and I'll start easy."
    if any(w in text for w in ("tired", "stuck", "can't", "cant")):
        return "That's okay. Let's shrink the task: just one small piece for five minutes. Which part feels hardest?"
    return "I'm with you. Tell me what you're working on and we'll go through it together."
