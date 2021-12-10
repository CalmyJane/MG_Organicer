import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

def main():

    root = Tk()
    frame = Frame(root)
    frame.grid(row=0, column=0, sticky="nsew")

    #bottomframe = Frame(root)
    #bottomframe.pack( side = BOTTOM )
    
    Frame()

    redbutton = Button(frame, text="Red", fg="red")
    redbutton.grid(row=0, column=0, sticky="ne", padx=1)

    greenbutton = Button(frame, text="Brown", fg="brown", padx=1)
    greenbutton.grid(row=0, column=1, sticky="ne")

    bluebutton = Button(frame, text="Blue", fg="blue", padx=1)
    bluebutton.grid(row=0, column=1, sticky="nw")

    blackbutton = Button(frame, text="Black", fg="black", padx=1)
    blackbutton.grid(row=1, column=0, sticky="ne")

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    root.mainloop()






    
#import wave

#af = wave.open('C:\\Users\\FreshBob\\Downloads\\Sample.wav', 'rb')
#af.setnchannels(1)
#af.setparams((1, 2, 22010, 0, 'NONE', 'Uncompressed'))
#audioData = af.readframes(1)
#print(audioData)
#af.close()

##af = wave.open('C:\\Users\\JGO\\Downloads\\TestSample_Formatted.wav', 'w')
##af.setnchannels(1)
##af.setparams((1, 2, 22010, 0, 'NONE', 'Uncompressed'))
##af.writeframes(audioData)
##af.close()


