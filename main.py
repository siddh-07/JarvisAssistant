import sys
import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import musicLibrary  


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

def processCommand(command):
    print(f"[User]: {command}")
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "time" in command and ("what" in command or "tell me" in command):
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
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
    elif "what is your name" in command or "who are you" in command:
        speak("I am Jarvis, Your personal AI assistant.")
    elif command.startswith("play"):
        song = command.replace("play", "", 1).strip()
        link = musicLibrary.music(song)
        webbrowser.open(link)
    elif command in ["exit", "quit", "stop","bye", "thank you"]:
        speak("Goodbye!")
        sys.exit()
    else:
        speak("Sorry, I didn't understand that command.")



if __name__ == "__main__":
    speak("Initializing Jarvis...")
    
    with sr.Microphone() as source:
        print("Adjusting for background noise... please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Ready.")

    while True:
        print("\n--- Waiting for 'Jarvis' ---")
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            word = recognizer.recognize_google(audio).lower()
            print(f"Heard: {word}")

            if word == "jarvis":
                speak("Yes, I'm listening.")

                # Listen for next command
                with sr.Microphone() as source:
                    print("--- Listening for command ---")
                    # It helps to re-adjust briefly before a specific command
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    # Added timeout here so it doesn't hang forever if you say nothing
                    audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)
                    command = recognizer.recognize_google(audio).lower()
                #  Process the command
                processCommand(command)
                
            elif word in ["exit", "quit", "stop","bye", "thank you"]:
                speak("Goodbye!")
                sys.exit()
        except sr.WaitTimeoutError:
            # Normal behavior if nobody speaks for a few seconds
            pass
        except sr.UnknownValueError:
            # Heard noise, but couldn't make out words.
            # Don't print error, just loop back and listen again.
            pass
        except Exception as e:
            # Only print real errors (like internet connection issues)
            print(f"An unexpected error occurred: {e}")