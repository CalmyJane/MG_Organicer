import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from PIL import *
from Knob import Knob

def main():

    root = Tk()
    # Add image file
    bg = PhotoImage(file = "images\\Menu_BG.png")
    root.minsize(width=bg.width()+10, height=bg.height()+10)
    root.resizable(False, False)
  
    # Show image using label
    bg_canvas = Canvas(root, width=bg.width()+5, height=bg.height()+5)
    bg_canvas.create_image(bg.width()/2+5, bg.height()/2+5, image=bg)
    knob = Knob(root, bg_canvas, 950, 150, 0, 127)
    bg_canvas.place(x = 0, y = 0)


    load_btn = Button(root, text="Load", fg="black",height= 1, width=10)
    load_btn.place(x=300, y=150)

    write_btn = Button(root, text="Write", fg="red", padx=1,height= 1, width=10)
    write_btn.place(x=150, y=150)



    #root.grid_rowconfigure(0, weight=1)
    #root.grid_columnconfigure(0, weight=1)

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


