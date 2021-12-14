import tkinter as tk
from tkinter import *
import os
import time
from Sample import Sample
from Preset import Preset
import Globals
from FileList import FileList
from tkinter import ttk
from UI import *


#Globals.SD_CARD_PATH = "C:\\Users\\FreshBob\\Documents\\Temp\\MicroGranny_Sample_Data\\"
Globals.SD_CARD_PATH = "C:\\MyData\\Python_Repos\\MG_Sampledata\\"
#Globals.SD_CARD_PATH = "G:\\"


main_ui = AppWindow()

main_ui.mainloop()




#import Playground
#Playground.main()
#from tkinter import * 
#from PIL import Image
#from PIL import ImageTk
#from PIL import *

#def onCanvasClick(event):
#    print('Got canvas click', event.x, event.y, event.widget)
#def onObjectClick(event):
#    print('Got object click', event.x, event.y, event.widget)
#    print(event.widget.find_closest(event.x, event.y))
     
#root = Tk()
#img_file = Image.open("images\\knob.png")
#img=ImageTk.PhotoImage(img_file)
#canvas = Canvas(root, width=100, height=200)
#img_canv=canvas.create_image(50, 150, image=img)
#canvas.tag_bind(img_canv, '<ButtonPress-1>', onObjectClick)


#obj1 = canvas.create_text(50, 30, text='Click me one')
#obj2 = canvas.create_text(50, 70, text='Click me two')
     
#canvas.bind('<Double-1>', onCanvasClick)                
#canvas.tag_bind(img_canv, '<Double-1>', onObjectClick)      
#canvas.tag_bind(obj2, '<Double-1>', onObjectClick)      
#canvas.pack()
#root.mainloop()