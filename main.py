import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
ttsx = pyttsx3.init()  

def speak(text):
    ttsx.say(text)
    ttsx.runAndWait()
    
def process_command(command):
    command = command.lower()
    
    if "open YouTube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open Google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    else:
        speak("Command not recognized. Please try again.")

if  __name__ == "__main__":
    speak("Initializing Jarvis.....")
    
    while True:
        # Listen for word "Jarvis"
        r = sr.Recognizer()
       
        try:
             with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Listening for 'Jarvis'...")
                audio = r.listen(source,timeout=5,phrase_time_limit=3)

                print("Recognizing...") 
                word = r.recognize_google(audio)
                print(f"User said: {word}")
                    
                if word.lower() == "jarvis":
                    speak("Yes, how can I help you?")
                    
                    # Listen for command
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=1)
                        print("Listening for command...")
                        audio = r.listen(source,timeout=5,phrase_time_limit=5)

                        print("Recognizing command...") 
                        command = r.recognize_google(audio)
                        print(f"User command: {command}")
                        
                        process_command(command)
            
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")  
        
            
    