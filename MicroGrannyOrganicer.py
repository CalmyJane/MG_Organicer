import tkinter as tk
from tkinter import *
import os
import time
from Sample import Sample
from Preset import Preset
import Globals
from FileList import FileList


Globals.SD_CARD_PATH = "C:\\Users\\FreshBob\\Documents\\Temp\\MicroGranny_Sample_Data\\"
#Globals.SD_CARD_PATH = "G:\"
sd_path = Globals.SD_CARD_PATH
preset = Preset(sd_path + "P01.txt")

file_list = FileList()
file_list.name_sample("A0.wav", "Test A0")
file_list.write_to_card()
file_list.read_card()

while True:
    pass
    time.sleep(0.1)



#root = tk.Tk()
#root.title("MicroGranny ORGANICER")
#root.iconbitmap("images/AppIcon.ico")
#root.resizable(False, False)
#root.wm_maxsize(700, 500)
#root.wm_minsize(700, 500)


#canvas = tk.Canvas(root, height=700, width=700, bg="#263042")
#canvas.pack()
#my_image = PhotoImage(file='images\RobBoss.png')
#canvas_image = canvas.create_image(0, 0, anchor = NW, image=my_image)
#root.mainloop()

