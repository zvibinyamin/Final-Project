#!/usr/bin/python3
from tkinter import *

import os
import os.path
import csv
import sqlite3
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter import filedialog

str1 = '                 '
str2 = '    '
frame = None
temp_Label =None
s = "c:\\Click_to_change.wav"

def FunForButtonASR(self):
    self.top = Toplevel()
    self.top.title("ASR")
    _Label1 = Label(self.top, text='Click the button below to activate the ASR:')
    _Label1.pack(padx=190, pady=30)
    _start_asr = Button(self.top, text=str2+'Start ASR'+str2)
    _start_asr.pack()
    _start_asr.config(font=("Courier", 12))
    Label(self.top, text=' ').pack(padx=190, pady=10)
    frame = Frame(self.top, borderwidth=5, relief="sunken", width=500, height=100)
    frame.pack()
    Label(self.top, text=' ').pack(padx=190, pady=10)
    Label(frame, text=' ').pack(padx=250, pady=5)
    temp_Label = Label(frame, text='\n\n')
    temp_Label.pack(padx=250, pady=5)

    def startGoogleASR(self):
        temp_Label.destroy()
        Label(frame, text='My name is zvika').pack()
        Label(frame, text=' ').pack(padx=250, pady=5)
    _start_asr.bind('<Button>', startGoogleASR)

def FunForButtonClassifier(self):
    self.top = Toplevel()
    self.top.title("Classifier")
    _Label1 = Label(self.top, text='Write the path of the file and Click the button below to activate the Classifier:')
    _Label1.pack(padx=90, pady=30)


    def update_btn_text():
        fname = askopenfilename(filetypes=(("TXT files", "*.txt"),("Template files", "*.tplate")))
        if fname:
            try:
                print("""here it comes: self.settings["template"].set(fname)""")
            except:  # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return
        s = "c:\\abc.wav"
        _change_path.set(str2 + 'Path: '+ s + str2)

    _change_path = tk.StringVar()
    btn = tk.Button(self.top, textvariable=_change_path, command=update_btn_text)
    _change_path.set(str2 + 'Path: '+ s + str2)

    btn.pack()

    Label(self.top, text=' ').pack()

    _start_asr = Button(self.top, text=str2+'Start Classifier'+str2)
    _start_asr.pack()
    _start_asr.config(font=("Courier", 12))

    Label(self.top, text=' ').pack(padx=190, pady=10)
    frame = Frame(self.top, borderwidth=5, relief="sunken", width=500, height=100)
    frame.pack()
    Label(self.top, text=' ').pack(padx=190, pady=10)
    Label(frame, text=' ').pack(padx=250, pady=5)
    temp_Label = Label(frame, text='\n\n')
    temp_Label.pack(padx=250, pady=5)

    def startGoogleASR(self):
        temp_Label.destroy()
        Label(frame, text='File: '+_Entry.get()+' text= My name is zvika.').pack()

        Label(frame, text=' ').pack(padx=250, pady=5)
    _start_asr.bind('<Button>', startGoogleASR)

def FunForButtonDTW(self):
    self.top = Toplevel()
    self.top.title("DTW")
    _Label1 = Label(self.top, text='Write the path of the file and Click the button below to activate the DTW:')
    _Label1.pack(padx=90, pady=30)
    _Entry = Entry(self.top)
    _Entry.pack(pady=5, padx=200)
    _Entry.insert(100, 'C:\\abcd.wav')
    _start_asr = Button(self.top, text=str2+'Start DTW'+str2)
    _start_asr.pack()
    _start_asr.config(font=("Courier", 12))
    Label(self.top, text=' ').pack(padx=190, pady=10)
    frame = Frame(self.top, borderwidth=5, relief="sunken", width=500, height=100)
    frame.pack()
    Label(self.top, text=' ').pack(padx=190, pady=10)
    Label(frame, text=' ').pack(padx=250, pady=5)
    temp_Label = Label(frame, text='\n\n')
    temp_Label.pack(padx=250, pady=5)

    def startGoogleASR(self):
        temp_Label.destroy()
        Label(frame, text='File: '+_Entry.get()+' text= My name is zvika.').pack()

        Label(frame, text=' ').pack(padx=250, pady=5)
    _start_asr.bind('<Button>', startGoogleASR)


root = Tk()
root.title("Final Project")

Label(root, text='\nPerpetrators by: Aviad Atlas, Zvika Binyamin, Akiva Gabay and Asaf Cohen.                                                    \n').pack()
Label4 = Label(root, text='\n\n Voice Recognition & Voice Emphasis\nUsing “Deep Learning"')
Label4.pack()
Label4.config(font=("Courier", 16))

Label(root, text=' ').pack(padx=10, pady=30, side=LEFT)


button_ASR = Button(root, text=str1+'ASR'+str1)
button_ASR.pack(padx=20, pady=50, side=LEFT)
button_ASR.bind('<Button>', FunForButtonASR)


button_Classifier = Button(root, text=str1+'Classifier'+str1)
button_Classifier.pack(padx=20, pady=50, side=LEFT)
button_Classifier.bind('<Button>', FunForButtonClassifier)

button_DTW = Button(root, text=str1+'DTW'+str1)
button_DTW.pack(padx=20, pady=50, side=LEFT)
button_DTW.bind('<Button>', FunForButtonDTW)

Label(root, text=' ').pack(padx=10, pady=30, side=LEFT)

mainloop()
