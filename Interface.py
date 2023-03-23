import tkinter as tk
from tkinter import ttk
from MainVA import VA
import threading

class RunVA(threading.Thread):
    def __init__(self):
        super(RunVA, self).__init__()

    def run(self):
        VA.main()

class GUI(tk.Tk):
    def __init__(self):
        super(GUI, self).__init__()
        self.title("Voice Assistant")
        self.geometry('700x700')
        self.config(padx=40, pady=40, bg="#4F98CA")

        self.va_img = tk.PhotoImage(file="va_icon.jpg")
        self.label1 = tk.Label(self, image=self.va_img, bg="#4F98CA")
        self.label1.place(x=180, y=0)
        self.mic = tk.PhotoImage(file="mic.png")
        self.speak = tk.Button(self, image=self.mic, highlightthickness=0, command=self.run_va, bg="#4F98CA")
        self.speak.place(x=260, y=520)
        self.label2 = tk.Label(self, bg="#4F98CA", fg="#37306B", text="Speak", font=("Courier", 24, "bold"))
        self.label2.place(x=240, y=590)

    def run_va(self):

        text = "Hello, try saying the following:\n\n  music\n  email\n  akinator\n  open youtube\n  where is (any " \
               "location)"
        self.label3 = tk.Label(self, bg="#4F98CA", fg="#F5EAEA", text=text, font=("Courier", 18, "bold"), justify="left")
        self.label3.place(x=100, y=310)

        va=RunVA()
        va.start()


if __name__=="__main__":
    gui=GUI()
    gui.mainloop()
