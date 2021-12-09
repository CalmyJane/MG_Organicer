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





# import required libraries
#from pydub import AudioSegment 
#from pydub.playback import play 
  
## Import an audio file 
## Format parameter only
## for readability 
#wav_file = AudioSegment.from_file(file = 'G:\\E2.WAV', format = "wav") 
  
## Play the audio file
#play(wav_file)