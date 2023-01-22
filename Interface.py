from tkinter import *
from tkinter import ttk
from MainVA import VA

root=Tk()
root.geometry('500x500')
root.title("VA Interface")


def va():
    VA.main()

Button(root,text='SPEAK',command=va).place(x=200,y=200)
root.mainloop()
