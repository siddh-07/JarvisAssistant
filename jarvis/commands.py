"""
jarvis/commands.py — Command Processor
Routes spoken commands to the appropriate handler.
"""

import sys
import datetime
import webbrowser
import pywhatkit

from jarvis.ai      import ask
from jarvis.weather import get_weather, format_weather
from jarvis.speech  import listen
from config import CMD_TIMEOUT, CMD_PHRASE_LIM


def process(command: str, on_reply=None, on_weather=None):
    """
    Process a user voice command and return a reply.

    Args:
        command:    Lowercased spoken command string.
        on_reply:   Callback(text) fired with the reply text.
        on_weather: Callback(data) fired with raw weather dict.

    Returns:
        Reply string.
    """
    reply = None

    # ---------- OPEN WEBSITES ----------
    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        reply = "Opening YouTube."

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        reply = "Opening Google."

    # ---------- TIME ----------
    elif "time" in command:
        now   = datetime.datetime.now()
        reply = f"The current time is {now.strftime('%I:%M %p')}."

    # ---------- WEATHER ----------
    elif "weather" in command:
        if "in" in command:
            city = command.split("in")[-1].strip()
        else:
            # Ask for city name
            ask_msg = "Which city's weather would you like to know?"
            if on_reply:
                on_reply(ask_msg)
            city = listen(timeout=CMD_TIMEOUT, phrase_limit=CMD_PHRASE_LIM)
            if not city:
                reply = "I didn't catch the city name. Please try again."
                if on_reply:
                    on_reply(reply)
                return reply

        data  = get_weather(city)
        reply = format_weather(data)

        # Fire weather card update if GUI is listening
        if on_weather and "error" not in data:
            on_weather(data)

    # ---------- IDENTITY ----------
    elif "your name" in command or "who are you" in command:
        reply = "I am Jarvis, your personal AI assistant."

    # ---------- PLAY MUSIC ----------
    elif command.startswith("play "):
        song = command.replace("play", "").strip()
        if song:
            query = song.replace(" ", "+")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            reply = f"Playing {song} on YouTube."
        else:
            reply = "What would you like me to play?"

    # ---------- EXIT ----------
    elif command in ["exit", "quit", "stop", "bye"]:
        reply = "Goodbye!"
        if on_reply:
            on_reply(reply)
        sys.exit()

    elif command in ["thank you", "thanks"]:
        reply = "You're most welcome!"
        if on_reply:
            on_reply(reply)
        sys.exit()

    # ---------- AI FALLBACK ----------
    else:
        reply = ask(command)

    if on_reply and reply:
        on_reply(reply)

    return reply