"""
Jarvis - Personal Voice Assistant
Author: Siddh Bhadani
Description:
A voice-controlled AI assistant using Speech Recognition, Text-to-Speech,
and OpenAI for intelligent responses.
"""

from dotenv import load_dotenv
import os
import sys
import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import pywhatkit
import requests
from openai import OpenAI
from typing import Optional

# ================== ENVIRONMENT SETUP ==================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY not found.")
    sys.exit(1)

if not WEATHER_API_KEY:
    print("ERROR: WEATHER_API_KEY not found.")
    sys.exit(1)

# ================== GLOBAL INITIALIZATION ==================

recognizer = sr.Recognizer()
openai_client = OpenAI()
is_speaking = False

# ================== HELPER FUNCTIONS ==================
def speak(text):
    print(f"[Jarvis]: {text}")
    try:
        global is_speaking
        is_speaking = True
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
        is_speaking = False
    except Exception as e:
        print(f"\n--- TTS ERROR: Could not speak. Error: {e} ---")

def get_weather(city: str) -> str:
    try:
        # Step 1: Get location key
        location_url = "http://dataservice.accuweather.com/locations/v1/cities/search"
        location_params = {"apikey": WEATHER_API_KEY, "q": city}
        response = requests.get(location_url, params=location_params)
        locations = response.json()

        if not locations:
            return f"Sorry, I couldn't find weather data for {city}."

        location_key = locations[0]["Key"]
        city_name = locations[0]["LocalizedName"]

        # Step 2: Get current weather
        weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
        weather_params = {"apikey": WEATHER_API_KEY, "details": True}
        weather_response = requests.get(weather_url, params=weather_params)
        data = weather_response.json()[0]

        temperature = data["Temperature"]["Metric"]["Value"]
        condition = data["WeatherText"]
        humidity = data["RelativeHumidity"]

        return (
            f"The current weather in {city_name} is {condition}. "
            f"The temperature is {temperature} degree Celsius "
            f"with humidity at {humidity} percent."
        )
    except Exception as e:
        print(f"\n--- WEATHER ERROR: {e} ---")
        return "Sorry, I couldn't fetch the weather right now."

def aiCommand(command: str) -> str:
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Jarvis, a friendly and smart personal assistant. "
                        "Answer concisely, clearly and in shorter form."
                    ),
                },
                {"role": "user", "content": command},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\n--- AI ERROR: {e} ---")
        return "Sorry, I am having trouble processing that right now."

def processCommand(command: str):
    """Process user voice commands"""
    print(f"[User]: {command}")

    # ---------- OPEN WEBSITES ----------
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    # ---------- TIME ----------
    elif "time" in command:
        now = datetime.datetime.now()
        speak(f"The current time is {now.strftime('%I:%M %p')}")

    # ---------- WEATHER ----------
    elif "weather" in command:
        if "in" in command:
            city = command.split("in")[-1].strip()
        else:
            speak("Which city's weather would you like to know?")
            city = listen(timeout=5, phrase_limit=5)
            if not city:
                speak("I didn't catch the city name.")
                return

        speak(f"Fetching weather for {city}")
        result = get_weather(city)
        speak(result)

    # ---------- IDENTITY ----------
    elif "your name" in command or "who are you" in command:
        speak("I am Jarvis, your personal AI assistant.")

    # ---------- PLAY MUSIC ----------
    elif command.startswith("play "):
        song = command.replace("play", "").strip()
        if song:
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
        else:
            speak("What should I play?")

    # ---------- EXIT ----------
    elif command in ["exit", "quit", "stop", "bye"]:
        speak("Goodbye!")
        sys.exit()

    elif command in ["thank you", "thanks"]:
        speak("You're most welcome!")
        sys.exit()

    # ---------- AI FALLBACK ----------
    else:
        speak(aiCommand(command))
        
def listen(timeout=5, phrase_limit=5) -> Optional[str]:
    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_limit
            )
        return recognizer.recognize_google(audio, language="en-IN").lower().strip()
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        print(f"Listening Error: {e}")
        return None

if __name__ == "__main__":
    speak("Initializing Jarvis")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    speak("Say Jarvis to wake me up")

    while True:
        if is_speaking:
            continue

        print("\n--- Waiting for wake word ---")
        word = listen()

        if not word:
            continue

        print(f"Heard: {word}")

        if "jarvis" in word:
            speak("Yes, How can I help you?")
            command = listen(timeout=8, phrase_limit=8)
            if command:
                processCommand(command)
            else:
                speak("I didn't catch that. Please say your command again.")
        elif word in ["exit", "quit", "stop", "bye"]:
            speak("Goodbye!")
            sys.exit()
        elif word in ["thank you", "thanks"]:
            speak("You're most welcome!")
            sys.exit()