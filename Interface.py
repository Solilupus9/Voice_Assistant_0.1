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
        self.geometry('500x500')
        ttk.Button(self,text='SPEAK',command=self.run_va).place(x=200,y=200)
        self.l=tk.Label(self,text='',borderwidth=1,relief='solid',height=8,width=28,anchor=tk.NW)
        self.l.place(x=150,y=250)

    def run_va(self):
        va=RunVA()
        va.start()

if __name__=="__main__":
    gui=GUI()
    gui.mainloop()
