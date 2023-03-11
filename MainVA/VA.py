import subprocess
import wolframalpha
import pyttsx3
import json
import random
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import smtplib
import ctypes
import time
import shutil
from urllib.request import urlopen


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour=int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am your Voice Assistant")


def username():
    speak("What should I call you sir?")
    uname = takeCommand()
    speak("Welcome ")
    speak(uname)
    columns = shutil.get_terminal_size().columns

    print("#####################".center(columns))
    print("Welcome Mr.", uname.center(columns))
    print("#####################".center(columns))

    speak("How can I help you?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,phrase_time_limit=4)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    file = open('datalog.txt')
    addpass = file.readlines()
    server.login(addpass[0],addpass[1])
    server.sendmail(addpass[0], to, content)
    file.close()
    server.close()


def main():
    clear = lambda: os.system('cls')
    clear()
    wishMe()
    username()

    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak("Here you go to Youtube\n")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Here you go to Google\n")
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            speak("Here you go to Stack Over flow.Happy coding")
            webbrowser.open("stackoverflow.com")

        elif 'music' in query or "song" in query:
            speak("Here you go with music")
            music_dir = "C:\\Users\\Aayush\\Music"
            songs = os.listdir(music_dir)
            print(songs)
            n=random.randint(1,len(songs))
            os.startfile(os.path.join(music_dir, songs[n]))

        elif 'time' in query:
            speak(f"Sir, the time is {datetime.datetime.now().strftime('%H:%M:%S')}")

        elif 'email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "esmail.s@somaiya.edu"
                sendEmail(to, content)
                speak("Email has been sent !")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        # elif 'send a mail' in query:
        #     try:
        #         speak("What should I say?")
        #         content = takeCommand()
        #         speak("To whom should I send")
        #         to = input()
        #         sendEmail(to, content)
        #         speak("Email has been sent !")
        #     except Exception as e:
        #         print(e)
        #         speak("I am not able to send this email")

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you?")
            query=takeCommand()
            if 'fine' in query or "good" in query:
                speak("That's wonderful!!")

        elif 'exit' in query:
            speak("Thank you for giving me your time")
            exit()

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        # elif "calculate" in query:
        #
        #     app_id = "App ID"
        #     client = wolframalpha.Client(app_id)
        #     indx = query.lower().split().index('calculate')
        #     query = query.split()[indx + 1:]
        #     res = client.query(' '.join(query))
        #     answer = next(res.results).text
        #     print("The answer is " + answer)
        #     speak("The answer is " + answer)

        elif 'search' in query or 'play' in query:
            query = query.replace("search", "")
            query = query.replace("play", "")
            webbrowser.open(query)

        elif "who i am" in query or 'who am i' in query:
            speak("If you talk then you are probably human.")

        # elif 'change background' in query:
        #     ctypes.windll.user32.SystemParametersInfoW(20,
        #                                                0,
        #                                                "Location of wallpaper",
        #                                                0)
        #     speak("Background changed successfully")

        elif 'news' in query:
            try:
                jsonObj=urlopen('''https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=\\times of India Api key\\''')
                data = json.load(jsonObj)
                i = 1
                speak('here are some top news India')
                print('''=============== TIMES OF INDIA ============''' + '\n')

                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:
                print(str(e))

        elif 'lock' in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif 'shutdown system' in query:
            speak("Are you sure?")
            query=takeCommand()
            try:
                if 'yes' in query:
                    speak("Shutting down")
                    subprocess.call('shutdown / p /f')
            except Exception as e:
                print(e)
                speak('Shutdown failed')

        # elif 'empty recycle bin' in query:
        #     winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        #     speak("Recycle Bin Recycled")

        elif "don't listen" in query or "stop listening" in query:
            speak("For how long?")
            a = int(takeCommand())
            print(a)
            time.sleep(a)

        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.nl/maps/place/"+location)

        elif "write a note" in query:
            speak("What should i write, sir")
            note = takeCommand()
            file = open('note.txt', 'w')
            speak("Should i include date and time?")
            snfm = takeCommand()
            if 'yes' in snfm:
                file.write(datetime.datetime.now().strftime("% H:% M:% S"))
                file.write(" :- \n")
            file.write(note)

        elif "show note" in query:
            speak("Showing Notes")
            file = open("note.txt", "r")
            print(file.read())
            speak(file.read(6))

        # elif "weather" in query:
        #
        #     # Google Open weather website
        #     # to get API of Open weather
        #     api_key = "Api key"
        #     base_url = "https://api.openweathermap.org / data / 2.5 / weather?"
        #     speak(" City name ")
        #     print("City name : ")
        #     city_name = takeCommand()
        #     complete_url = base_url + "appid =" + api_key + "&q =" + city_name
        #     response = requests.get(complete_url)
        #     x = response.json()
        #
        #     if x["code"] != "404":
        #         y = x["main"]
        #         current_temperature = y["temp"]
        #         current_pressure = y["pressure"]
        #         current_humidiy = y["humidity"]
        #         z = x["weather"]
        #         weather_description = z[0]["description"]
        #         print(" Temperature (in kelvin unit) = " + str(
        #             current_temperature) + "\n atmospheric pressure (in hPa unit) =" + str(
        #             current_pressure) + "\n humidity (in percentage) = " + str(
        #             current_humidiy) + "\n description = " + str(weather_description))
        #
        #     else:
        #         speak(" City Not Found ")