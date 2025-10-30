import pyttsx3

engine = pyttsx3.init()
engine.say("Testing text to speech. If you hear this, drivers are fine.")
engine.runAndWait()