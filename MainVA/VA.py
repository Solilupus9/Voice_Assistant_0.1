import re
import subprocess
import wolframalpha
import pyttsx3
import random
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pyjokes
import ctypes
import time
import urllib.request
from akinator import *
import yagmail
from gcsa.google_calendar import GoogleCalendar
from gcsa.reminders import EmailReminder,PopupReminder
from gcsa.event import Event
from beautiful_date import hours

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

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
    time.sleep(0.5)

def takeCommand(ltime=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,phrase_time_limit=ltime)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query


def sendEmail(to,sub, content):
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
    # server.starttls()
    # print(os.getcwd())
    # file = open('./MainVA/datalog.txt','r')
    # addpass = file.readlines()
    # server.login(addpass[0],addpass[1])
    # server.sendmail(addpass[0], to, content)
    # file.close()
    # server.close()
    file = open('./MainVA/datalog.txt','r')
    addpass = file.readlines()
    yagmail.SMTP(addpass[0],addpass[1]).send(to,sub,content)
    file.close()

def main():
    clear = lambda: os.system('cls')
    clear()
    wishMe()
    speak("Please tell me how I can help you?")

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
                speak('What is the subject?')
                sub=takeCommand()
                speak("Please tell me what you wish to write.")
                content=takeCommand()
                speak('Do you want to type recipient email id?')
                query = takeCommand()
                if 'no' in query:
                    speak('Please tell me the email id')
                    to=takeCommand()
                else:
                    speak('Please type the email id')
                    to=input("Enter email id:")
                sendEmail(to,sub, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you?")
            query=takeCommand()
            if 'fine' in query or "good" in query:
                speak("That's wonderful!")

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

        elif 'search' in query and 'on youtube' in query:
            key=query.replace('search ','').replace(' on youtube','').replace(' ','+')
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+key)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])

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

        elif 'lock' in query and 'device' in query:
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

        elif "don't listen" in query or "stop listening" in query:
            speak("For how long?")
            a = str(takeCommand())
            print(a)
            if 'second' in a:
                a=a.replace(' seconds','')
                a=a.replace(' second','')
                time.sleep(int(a))
            elif 'minute' in a:
                a = a.replace(' minutes', '')
                a = a.replace(' minute', '')
                time.sleep(int(a)*60)
            else:
                speak("Invalid time")
            speak('I am listening again')

        elif "where is" in query:
            query = query.replace("where is", "")
            speak("User asked to Locate"+query)
            webbrowser.open("https://www.google.nl/maps/place/"+query)

        elif "write a note" in query:
            speak("What should I name it?")
            name=takeCommand()
            speak("What should i write?")
            note = takeCommand()
            file = open(name+'.txt', 'a')
            speak("Should I include date and time?")
            snfm = takeCommand()
            if 'yes' in snfm:
                file.write(datetime.datetime.now().strftime("% H:% M:% S"))
                file.write(" :- \n")
            file.write(note)
            file.close()

        elif "show note" in query:
            speak("Which note do you want me to show?")
            name=takeCommand()
            try:
                speak(f"Opening {name}")
                file = open(name+".txt", "r")
                print(file.read())
                speak(file.read(6))
            except Exception as e:
                print(e)
                speak(f'{name} could not be opened')

        elif 'chess' in query:
            webbrowser.open('https://www.chess.com/play/computer')

        elif 'akinator' in query:
            speak('Playing Akinator')
            aki=Akinator()
            q=aki.start_game()
            speak('First question:')
            try:
                while aki.progression<=80:
                    print(q)
                    speak(q)
                    a=takeCommand()
                    if 'yes' in a:
                        q=aki.answer('yes')
                    elif 'no' in a:
                        q=aki.answer('no')
                    elif 'dont know' in a:
                        q=aki.answer('i')
                    elif 'probably' in a or 'think so' in a:
                        q=aki.answer('p')
                    elif 'probably not' in a or 'dont think so' in a:
                        q=aki.answer('pn')
                    elif 'back' in a:
                        try:
                            speak('Previous question:')
                            q=aki.back()
                        except CantGoBackAnyFurther:
                            speak('There are no previous questions')
                    else:
                        speak('That is not a valid answer')
            except Exception as e:
                print(e)
                speak("An error hs occurred")

            aki.win()
            speak('I have an answer for you')
            print(aki.first_guess)
            speak(f"It is {aki.first_guess['name']}.{aki.first_guess['description'] if aki.first_guess['description'] != '---' else ''}!")
            speak('Am I correct?')
            query=takeCommand()
            if 'yes' in query:
                speak('Of course I am!')
                speak('Thank you for playing with me.')
            elif 'no' in query:
                speak("Oops. I am sorry.")

        # elif 'reminder' in query:
        #     gc=GoogleCalendar(credentials_path='./credentials.json')
        #     speak('What should I set reminder for?')
        #     title=takeCommand()
        #     speak('On what day?')
        #     q=takeCommand()
        #     rep={'first':'1','second':'2','third':'3','th':'','rd':'','nd':'','st':''}
        #     for i,j in rep.items():
        #         q=q.replace(i,j)
        #     d=datetime.datetime.strptime(q+' 2023','%d %B %Y')
        #     print(d.date())
        #     speak('At what time?')
        #     t = takeCommand()
        #     t = str(list(t).insert(2, ':')) if ':' not in t else t
        #     t='0'+t if len(t)==4 else t
        #     d=d.replace(hour=int(t[:2]),minute=int(t[3:]))
        #     e=Event(title,
        #             start=d,
        #             end=d+2*hours,
        #             reminders=[
        #                 EmailReminder(minutes_before_start=15),
        #                 PopupReminder(minutes_before_start=15)
        #             ])
        #     gc.add_event(e)
        #     speak(f"Remainder for {title} has been set on {d.strftime('%d %B')} at {d.strftime('%H %M')}")

        elif 'event' in query:
            gc=GoogleCalendar(credentials_path='./credentials.json')
            speak('What should be the title of the event?')
            title=takeCommand()
            speak('On what day?')
            q = takeCommand()
            rep = {'first': '1', 'second': '2', 'third': '3', 'th': '', 'rd': '', 'nd': '', 'st': ''}
            for i, j in rep.items():
                q = q.replace(i, j)
            d = datetime.datetime.strptime(q + ' 2023', '%d %B %Y')
            speak('At what time does the event start?')
            t = takeCommand()
            t = str(list(t).insert(2, ':')) if ':' not in t else t
            t = '0' + t if len(t) == 4 else t
            d = d.replace(hour=int(t[:2]), minute=int(t[3:]))
            speak('At what time does the event end?')
            e = takeCommand()
            e = str(list(e).insert(2, ':')) if ':' not in e else e
            e = '0' + e if len(e) == 4 else e
            d = d.replace(hour=int(e[:2]), minute=int(e[3:]))
            speak('Do you want me to set a reminder?')
            q=takeCommand()
            if 'yes' in q:
                e=Event(title,
                        start=d,
                        end=e,
                        reminders=[
                            EmailReminder(minutes_before_start=15),
                            PopupReminder(minutes_before_start=15)
                        ])
            else:
                e=Event(title,
                        start=d,
                        end=e)
            gc.add_event(e)
            speak(f"Remainder for {title} has been set on {d.strftime('%d %B')} at {d.strftime('%H %M')}")

        elif query=="none":
            continue

        else:
            speak("Sorry, I could not understand that")