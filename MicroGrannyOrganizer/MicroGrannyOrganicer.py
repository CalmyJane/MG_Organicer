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


Globals.SD_CARD_PATH = "C:\\Users\\FreshBob\\Documents\\Temp\\MicroGranny_Sample_Data\\"
#Globals.SD_CARD_PATH = "G:\"

file_list = FileList()
file_list.name_file("A0.wav", "Test A23")
file_list.name_file("P01.TXT", "Test preset A23")
main_ui = AppWindow(file_list)
main_ui.set_samples(file_list.samples)
main_ui.mainloop()

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


