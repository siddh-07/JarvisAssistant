"""
jarvis/ai.py — AI Command Handler
Sends user commands to OpenAI and returns intelligent responses.
"""

from openai import OpenAI
from config import OPENAI_API_KEY, AI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "You are Jarvis, a friendly and smart personal assistant. "
    "Answer concisely, clearly and in shorter form."
)


def ask(command: str) -> str:
    """
    Send a command to OpenAI and return the response.

    Args:
        command: The user's spoken command/question.

    Returns:
        AI-generated response string.
    """
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": command},
            ],
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[AI Error]: {e}")
        return "Sorry, I'm having trouble processing that right now."