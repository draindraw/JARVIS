import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import time

recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000  # reduce sensitivity
recognizer.dynamic_energy_threshold = True
engine = pyttsx3.init()
news_api_key = "APIKEY" 

def speak(text):
    temp_engine = pyttsx3.init()   # use fresh engine each time
    temp_engine.say(text)
    temp_engine.runAndWait()
    temp_engine.stop()
    time.sleep(0.6)   # ensure driver releases before listening

def processCommand(c):
    if("open google" in c.lower()):
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif("open youtube" in c.lower()):
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif("open facebook" in c.lower()):
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif("open instagram" in c.lower()):
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif(c.lower().startswith("play")):
        song=c.lower().split(" ")[1]
        link=musicLibrary.music[song]
        webbrowser.open(link)

    elif("news" in c.lower()):
     r=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}")
     if r.status_code == 200:   # success
        data = r.json()  # parse JSON response
        articles = data.get("articles", [])
        
        print("Top Headlines:\n")
        for i, article in enumerate(articles, start=1):
            speak(article["title"])



if __name__ == "__main__":
    speak("Initializing Jarvis....")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word 'Jarvis'...")
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Helps reduce noise issues
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Yes, how can I help you?")
                time.sleep(0.8)
                with sr.Microphone() as source:
                    print("Jarvis Active... Listening for command...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command received: {command}")
                    processCommand(command)

        except sr.WaitTimeoutError:
            print("Listening timed out, waiting again...")
            continue
        except sr.UnknownValueError:
            print("Could not understand audio")
            continue
        except Exception as e:

            print(f"Error: {e}")
