import pyttsx3
print("Testing audio engine...")
engine = pyttsx3.init()
# On some systems, setting properties explicitly helps kickstart it
engine.setProperty('rate', 150) 
engine.setProperty('volume', 1.0) 

engine.say("Hello. If you can hear this, my voice is working.")
engine.runAndWait()
print("Test complete.")