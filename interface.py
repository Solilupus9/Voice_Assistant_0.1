from tkinter import *


def speak():
    listen()


def listen():
    if listening_text["text"] == "Listening.....":
        listening_text.config(text="Press Button to Speak")
        listening_text.place(x=0, y=100)
    elif listening_text["text"] == "Press Button to Speak":
        listening_text["text"] = "Listening"
        listening_text.place(x=100, y=100)
        window.after(1000, listen)
    else:
        listening_text["text"] += "."
        window.after(1000, listen)


def emailEntry():
    pass


window = Tk()
window.title("VA Interface")
window.minsize(height=600, width=600)
window.config(padx=50, pady=50, background="#2C3333")

listening_text = Label(pady=80, text="Press Button to Speak", fg="#CBE4DE", bg="#2C3333", font=("Courier", 30, "bold"))
listening_text.place(x=0, y=100)

mic = PhotoImage(file="mic.png")

mic_button = Button(image=mic, highlightthickness=0, command=speak)
mic_button.place(x=210, y=300)

window.mainloop()
