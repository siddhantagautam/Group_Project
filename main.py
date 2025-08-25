import speech_recognition as sr
import webbrowser as web
import pyttsx3 as tts 
from google import genai

from urllib.parse import quote
import requests
import re 

import os, platform, subprocess

recognizer = sr.Recognizer()
engine = tts.init()




def play_first_youtube_video(query):
    search_url = f"https://www.youtube.com/results?search_query={quote(query)}"
    response = requests.get(search_url).text
    match = re.search(r'\/watch\?v=[\w-]+', response)
    if match:
        video_url = "https://www.youtube.com" + match.group(0)
        web.open(video_url)
    else:
        speak("Video not found.")

def processCommand(c):
     c_lower = c.lower()
     if "youtube" in c_lower or "play" in c_lower:
        if "play" in c_lower:
            words = c_lower.split()

            # Remove filler words ("from youtube", "on youtube")
            if "from" in words:
                from_index = words.index("from")
                query = " ".join(words[words.index("play")+1:from_index])
            elif "on" in words:
                on_index = words.index("on")
                query = " ".join(words[words.index("play")+1:on_index])
            elif "youtube" in words:
                yt_index = words.index("youtube")
                query = " ".join(words[words.index("play")+1:yt_index])
            else:
                # just "play song" → default YouTube
                query = " ".join(words[words.index("play")+1:])

            if query.strip():
                play_first_youtube_video(query)
            else:
                web.open("https://youtube.com")
        else:
            web.open("https://youtube.com")

     elif "open facebook" in c_lower:
        web.open("https://facebook.com")

     elif "open instagram" in c_lower:
        web.open("https://instagram.com")

     elif "open whatsapp" in c_lower:
        web.open("https://whatsapp.com")

     elif "open linkidin" in c_lower:
        web.open("https://linkidin.com")

     elif "open" in c_lower:
         app = c_lower.replace("open", "").strip()
         system = platform.system()

         if app:
            speak(f" opening {app}")
            try:
                if system == "Darwin": #for mac os
                    subprocess.call(["open", "-a", app])
                elif system == "windows":
                    os.system(f"start {app}")
                else:
                    speak("sorry, OS not supported")
            except Exception as e:
                speak(f"failed to open {app}")
         

     else:
       client = genai.Client(api_key="AIzaSyBZGVdDSwUlAKR3bXZZtAeviIl_i9Adl1Y")

       response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"suppose you are my personal assistance named jarvis, and answer in not too short, not too long  {c}"
        )
       speak(response.text)
       print(response.text)
         

def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Initilizing Jarvish.. ")
    while True:
    #     # listun to the word jarvis.
    #     # get audio from the microphone
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            print("Recognizing...")
            word = recognizer.recognize_google(audio, language = "en-IN")

            if "jarvis" in word.lower():
                speak("Ya...")
                # wait for next word
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = recognizer.listen(source)
                    comand = recognizer.recognize_google(audio, timeout = 10)
                    print(comand)
                    processCommand(comand)

        except Exception as e:
            print("Error; {0}".format(e))









