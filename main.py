import speech_recognition as sr 
import webbrowser 
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os


# Initialize the recognizer

r = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "2c83e034978243898d219edda036c839"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")



def aiProcess(command):
    client = OpenAI(api_key="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")
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud Give short response"},
      {"role": "user", "content": command}
    ]
    )
    return  completion.choices[0].message.content 


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "play" in c.lower():
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()

            articles = data.get('articles', [])

            for article in articles:
                speak(article['title'])

    else:
        output = aiProcess(c)
        speak(output)

 


if __name__ == "__main__":
    # Ask the user to say "Speak Now"
    speak("Initializing Jarvis......")
    while True:
        r = sr.Recognizer()
            

        print("recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening.....")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                
                with sr.Microphone() as source:
                    print("Jarvis Active.....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                        
                    processCommand(command)
    
        except Exception as e:
            print("error; {0}".format(e))




         