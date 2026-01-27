from dotenv import load_dotenv
import os
import sys
import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime 
import pywhatkit 
import openai

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize global engines once
recognizer = sr.Recognizer()

# --- Initialization of TTS ---
def speak(text):
    print(f"[Jarvis]: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150) 
        # Optional:change voice if needed
        # voices = engine.getProperty('voices')
        # engine.setProperty('voice', voices[1].id) 
        engine.say(text)
        engine.runAndWait()
        #Explicitly stop the engine loop to release resources
        engine.stop()
    except Exception as e:
        print(f"\n--- TTS ERROR: Could not speak. Error: {e} ---")
        
def aiCommand(text):
    client = openai.Client(API_KEY)
    



def processCommand(command):
    print(f"[User]: {command}")
    
    # Open YouTube
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    
    # Open Google
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    
    # Tell the time
    elif "time" in command and ("what" in command or "tell me" in command):
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    
    # Search in Google
    elif "search for" in command:
        try:
            # Grab whatever is after "search for"
            search_term = command.split("search for", 1)[1].strip()
            if search_term:
                speak(f"Searching Google for {search_term}")
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
            else:
                speak("I heard 'search for', but nothing after it.")
        except IndexError:
             speak("Sorry, I didn't catch the search term.")
    
    # Tell info about JARVIS
    elif "what is your name" in command or "who are you" in command:
        speak("I am Jarvis, Your personal AI assistant.")
    
    # Play music from Youtube
    elif command.startswith("play "):
        try:
            song = command.replace("play", "").strip()
            
            if song:
                speak(f"Okay, playing {song} on YouTube.")
                # This single line does the search and opens the browser
                pywhatkit.playonyt(song)
            else:
                speak("What did you want me to play?")
        except Exception as e:
             speak("Sorry, I encountered an issue trying to play that.")
             print(f"Error with pywhatkit: {e}")
                
    # Exit command
    elif command in ["exit", "quit", "stop", "bye", "thank you"]:
        speak("Goodbye!")
        sys.exit()
    else:
        speak("Sorry, I didn't understand that command.")



if __name__ == "__main__":
    speak("Initializing Jarvis...")
    
    with sr.Microphone() as source:
        print("Adjusting for background noise... please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.8
        print("Ready... you can say 'Jarvis' to wake me up.")

    while True:
        print("\n--- Waiting for 'Jarvis' ---")
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            word = recognizer.recognize_google(audio, language="en-IN").lower().strip()
            print(f"Heard: {word}")

            if "jarvis" in word:
                speak("Yes, how can I help you?")

                # Listen for next command
                with sr.Microphone() as source:
                    print("--- Listening for command ---")
                    # It helps to re-adjust briefly before a specific command
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    recognizer.energy_threshold = 300
                    recognizer.dynamic_energy_threshold = True
                    recognizer.pause_threshold = 0.8

                    # Added timeout here so it doesn't hang forever if you say nothing
                    audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)
                    command = recognizer.recognize_google(audio, language="en-IN").lower().strip()
                #  Process the command
                processCommand(command)
            elif word in ["exit", "quit", "stop", "bye", "thank you"]:
                speak("Goodbye!")
                sys.exit()
        except sr.WaitTimeoutError:
            # Normal behavior if nobody speaks for a few seconds
            pass
        except sr.UnknownValueError:
            # Could not understand audio
            pass
        except Exception as e:
            # Only print real errors (like internet connection issues)
            print(f"An unexpected error occurred: {e}")