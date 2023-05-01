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
import tkinter as tk
import threading

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

class RunVA(threading.Thread):
    def __init__(self):
        super(RunVA, self).__init__()

    def run(self):
        main()
def run_va():
    va=RunVA()
    va.start()

root=tk.Tk()
root.title('Voice Assistant')
root.geometry('700x700+200-100')
root.config(padx=40,pady=40,bg="#4F98CA")
va_img = tk.PhotoImage(file="../va_icon.jpg")
label1 = tk.Label(root, image=va_img, bg="#4F98CA")
label1.place(x=180, y=0)
mic = tk.PhotoImage(file="../mic.png")
speak = tk.Button(root, image=mic, highlightthickness=0, bg="#4F98CA",command=run_va)
speak.place(x=260, y=520)
label2 = tk.Label(root, bg="#4F98CA", fg="#37306B", text="Speak", font=("Courier", 24, "bold"))
label2.place(x=240, y=590)
text = "Things you can do:\n\n  music\n  email\n  akinator\n  open youtube\n  where is (any " \
       "location)"
label3 = tk.Label(root, bg="#4F98CA", fg="#F5EAEA", text=text, font=("Courier", 18, "bold"), justify="left")
label3.place(x=100,y=310)

to=tk.StringVar()

def getemail(x:tk.Entry):
    global to
    to=x.get()

def ct(show:str):
    label3.config(text=show)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        ct("Good Morning!!")
        speak("Good Morning!")
    elif 12 <= hour < 18:
        ct("Good Afternoon!")
        speak("Good Afternoon!")
    else:
        ct("Good Evening!")
        speak("Good Evening!")
    ct("I am your Voice Assistant")
    speak("I am your Voice Assistant")
    time.sleep(0.5)

def takeCommand(ltime=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        ct("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,phrase_time_limit=ltime)
    try:
        ct("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print(e)
        print("Unable to recognize voice")
        return "None"
    return query


def sendEmail(to,sub, content):
    file = open('./datalog.txt','r')
    addpass = file.readlines()
    yagmail.SMTP(addpass[0],addpass[1]).send(to,sub,content)
    file.close()

def main():
    clear = lambda: os.system('cls')
    clear()
    wishMe()
    ct("Please tell me how I can help you?")
    speak("Please tell me how I can help you?")

    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            ct('Searching Wikipedia...')
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            ct(results)
            speak(results)

        elif 'open youtube' in query:
            ct("Here you go to Youtube")
            speak("Here you go to Youtube")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            ct("Here you go to Google")
            speak("Here you go to Google")
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            ct("Here you go to Stack Over flow")
            speak("Here you go to Stack Over flow")
            webbrowser.open("stackoverflow.com")

        elif 'music' in query or "song" in query:
            speak("Here you go with music")
            music_dir = "C:\\Users\\Aayush\\Music"#CHANGE DIRECTORY
            songs = os.listdir(music_dir)
            print(songs)
            n=random.randint(1,len(songs))
            ct(f"Playing: {songs[n]}")
            os.startfile(os.path.join(music_dir, songs[n]))

        elif 'time' in query:
            ct(f"Current time is {datetime.datetime.now().strftime('%H:%M')}")
            speak(f"Current time is {datetime.datetime.now().strftime('%H:%M')}")

        elif 'email' in query:
            try:
                global to
                ct('What is the subject?')
                speak('What is the subject?')
                sub=takeCommand()
                ct("Please tell me what you wish to write")
                speak("Please tell me what you wish to write")
                content=takeCommand()
                speak('Do you want to type recipient email id?')
                query = takeCommand()
                if 'no' in query:
                    ct('Please tell me the email id')
                    speak('Please tell me the email id')
                    to=takeCommand()
                else:
                    speak('Please type the email id')
                    x=tk.Entry(root,textvariable=to,width=30,font=("Courier", 18))
                    x.place(x=100,y=350)
                    a=tk.Button(root,text='Submit',command=lambda:getemail(x),height=2,width=10)
                    a.place(x=280,y=400)
                    time.sleep(15)
                    a.destroy()
                    x.destroy()
                sendEmail(to,sub, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                ct("I am not able to send this email")
                speak("I am not able to send this email")

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you?")
            query=takeCommand()
            if 'fine' in query or "good" in query:
                speak("That's wonderful!")

        elif 'exit' in query:
            ct("Thank you for giving me your time")
            speak("Thank you for giving me your time")
            exit()

        elif 'joke' in query:
            j=pyjokes.get_joke()
            ct(j)
            speak(j)

        elif "calculate" in query:

            app_id = ""
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is " + answer)
            speak("The answer is " + answer)

        elif 'search' in query or 'play'in query and 'on youtube' in query:
            key=query.replace('search ','').replace(' on youtube','').replace(' ','+')
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+key)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])

        elif "who i am" in query or 'who am i' in query:
            speak("If you talk then you are probably human.")

        # elif 'change background' in query:
        #     ctypes.windll.user32.SystemParametersInfoW(20,
        #                                                0,
        #                                                "Location of wallpaper",
        #                                                0)
        #     speak("Background changed successfully")

        elif 'lock' in query and 'device' in query:
            ct("Locking the device")
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif 'shutdown system' in query:
            ct("Are you sure?")
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
            ct("For how long?")
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
            ct("What should I name it?")
            speak("What should I name it?")
            name=takeCommand()
            ct("What should i write?")
            speak("What should i write?")
            note = takeCommand()
            file = open(name+'.txt', 'a')
            ct("Should I include date and time?")
            speak("Should I include date and time?")
            snfm = takeCommand()
            if 'yes' in snfm:
                file.write(datetime.datetime.now().strftime("% H:% M:% S"))
                file.write(" :- \n")
            file.write(note)
            file.close()

        elif "show note" in query:
            ct("Which note do you want me to show?")
            speak("Which note do you want me to show?")
            name=takeCommand()
            try:
                ct(f"Opening {name}")
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
            ct('Playing Akinator')
            speak('Playing Akinator')
            aki=Akinator()
            q=aki.start_game()
            speak('First question:')
            try:
                while aki.progression<=80:
                    ct(q)
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
                            ct('Previous question:')
                            speak('Previous question:')
                            q=aki.back()
                        except CantGoBackAnyFurther:
                            ct('There are no previous questions')
                            speak('There are no previous questions')
                    else:
                        ct('That is not a valid answer')
                        speak('That is not a valid answer')
            except Exception as e:
                print(e)
                speak("An error hs occurred")

            aki.win()
            speak('I have an answer for you')
            print(aki.first_guess)
            ct(f"It is {aki.first_guess['name']}.{aki.first_guess['description'] if aki.first_guess['description'] != '---' else ''}!")
            speak(f"It is {aki.first_guess['name']}.{aki.first_guess['description'] if aki.first_guess['description'] != '---' else ''}!")
            speak('Am I correct?')
            query=takeCommand()
            if 'yes' in query:
                speak('Of course I am!')
                speak('Thank you for playing with me.')
            elif 'no' in query:
                speak("Oops. I am sorry.")

        elif 'event' in query:
            gc=GoogleCalendar(credentials_path='./credentials.json')
            ct('What should be the title of the event?')
            speak('What should be the title of the event?')
            title=takeCommand()
            ct('On what day?')
            speak('On what day?')
            q = takeCommand()
            rep = {'first': '1', 'second': '2', 'third': '3', 'th': '', 'rd': '', 'nd': '', 'st': ''}
            for i, j in rep.items():
                q = q.replace(i, j)
            d = datetime.datetime.strptime(q + ' 2023', '%d %B %Y')
            ct('At what time does the event start?')
            speak('At what time does the event start?')
            t = takeCommand()
            t = str(list(t).insert(2, ':')) if ':' not in t else t
            t = '0' + t if len(t) == 4 else t
            d = d.replace(hour=int(t[:2]), minute=int(t[3:]))
            ct('At what time does the event end?')
            speak('At what time does the event end?')
            e = takeCommand()
            e = str(list(e).insert(2, ':')) if ':' not in e else e
            e = '0' + e if len(e) == 4 else e
            d = d.replace(hour=int(e[:2]), minute=int(e[3:]))
            ct('Do you want me to set a reminder?')
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
            ct(f"Remainder for {title} has been set on {d.strftime('%d %B')} at {d.strftime('%H %M')}")
            speak(f"Remainder for {title} has been set on {d.strftime('%d %B')} at {d.strftime('%H %M')}")

        elif 'search' in query or 'play' in query:
            query = query.replace("search", "")
            query = query.replace("play", "")
            webbrowser.open(query)

        elif query=="none":
            continue

        else:
            speak("Sorry, I could not understand that")

if __name__=='__main__':
    root.mainloop()