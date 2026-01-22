import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime # Import datetime at the top

# Initialize global engines once
recognizer = sr.Recognizer()
ttsx = pyttsx3.init()

# Optional: Configure voice (make it speak faster or change voice)
ttsx.setProperty('voice', 1.0) # Change index for different voices
ttsx.setProperty('rate', 150) # Speed up a bit

def speak(text):
    """Function to convert text to speech"""
    print(f"[Jarvis]: {text}")
    ttsx.say(text)
    ttsx.runAndWait()

def processCommand(command):
    print(f"[User]: {command}")
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "what time is it" in command:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        speak(f"The current time is {current_time}")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't understand that command.")    
    

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    
    while True:
        r = sr.Recognizer()
        print("Recognizing...")
        
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source , timeout=2, phrase_time_limit=1)
            word = recognizer.recognize_google(audio).lower()
            
            if(word == "jarvis"):
                speak("Yaa..")
                
                #Listen for next command
                with sr.Microphone() as source:
                    print("Jarvis Activated...")
                    audio = recognizer.listen(source , timeout=2, phrase_time_limit=1)
                    command = recognizer.recognize_google(audio).lower()
                
                processCommand(command)
                
            elif(word == "exit" or word == "quit"):
                speak("Goodbye!")
                exit()
        except Exception as e:
            print("Error:", str(e))