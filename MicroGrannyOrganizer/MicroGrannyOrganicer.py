import os
import Globals
from UI import *
from tkinter import filedialog as fd



target_folder = fd.askdirectory(title="Select Folder or SD-Card to work on")

#target_folder = "C:\\Users\\FreshBob\\Documents\\Temp\\MicroGranny_Sample_Data\\"
#target_folder = "C:\\MyData\\Python_Repos\\MG_Sampledata\\"
#target_folder = "G:\\"
if target_folder:
    Globals.SD_CARD_PATH = target_folder+'\\'
    main_ui = AppWindow()
    main_ui.mainloop()
