"""
jarvis/commands.py — Command Processor
Routes spoken commands to the appropriate handler.
"""

import datetime
import webbrowser
import threading

from jarvis.ai      import ask
from jarvis.weather import get_weather, format_weather
from jarvis.speech  import listen
from config import CMD_TIMEOUT, CMD_PHRASE_LIM

# Selenium is imported lazily inside play_on_youtube()
# so startup time is not affected if it's never used


def play_on_youtube(song: str):
    """
    Open Chrome via Selenium, search YouTube, and auto-play the first result.
    Runs in a background thread so it never blocks Jarvis.
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--mute-audio")        # start muted to avoid autoplay block
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )

        query = song.replace(" ", "+")
        driver.get(f"https://www.youtube.com/results?search_query={query}")

        # Wait for first video thumbnail and click it
        first_video = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "ytd-video-renderer a#thumbnail")
            )
        )
        driver.execute_script("arguments[0].click();", first_video)

        # Unmute after navigation
        import time
        time.sleep(2)
        driver.execute_script(
            "document.querySelector('video').muted = false;"
            "document.querySelector('video').volume = 1;"
        )

    except Exception as e:
        print(f"[YouTube Error]: {e}")


def process(command: str, on_reply=None, on_weather=None, on_exit=None):
    """
    Process a user voice command and return a reply.

    Args:
        command:    Lowercased spoken command string.
        on_reply:   Callback(text) fired with the reply text.
        on_weather: Callback(data) fired with raw weather dict.
        on_exit:    Callback fired when user says goodbye (lets GUI close cleanly).

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

        if on_weather and "error" not in data:
            on_weather(data)

    # ---------- IDENTITY ----------
    elif "your name" in command or "who are you" in command:
        reply = "I am Jarvis, your personal AI assistant."

    # ---------- PLAY MUSIC (Selenium) ----------
    elif "play" in command:
        song = command.replace("play", "").strip()
        if song:
            reply = f"Playing {song} on YouTube."
            if on_reply:
                on_reply(reply)
            # Launch selenium in background so Jarvis stays responsive
            threading.Thread(
                target=play_on_youtube, args=(song,), daemon=True
            ).start()
            return reply
        else:
            reply = "What would you like me to play?"

    # ---------- EXIT ----------
    elif command in ["exit", "quit", "stop", "bye"]:
        reply = "Goodbye!"
        if on_reply:
            on_reply(reply)
        if on_exit:
            on_exit()
        return reply

    elif command in ["thank you", "thanks"]:
        reply = "You're most welcome!"
        if on_reply:
            on_reply(reply)
        if on_exit:
            on_exit()
        return reply

    # ---------- AI FALLBACK ----------
    else:
        reply = ask(command)

    if on_reply and reply:
        on_reply(reply)

    return reply