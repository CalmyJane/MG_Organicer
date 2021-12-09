import shutil
import os
from collections import namedtuple 
import Globals
import json





class CardFile(object):
    """Abstract class, represents a file on the MicroGrannys SD-Card. Can bei either a Preset ("P01.txt") a Sample ("A0.wav") or NameTable ("NameTable.txt")"""

    path = ""             ## Path without Filename, may be path on Card or path on Drive. Files no computer CAN NOT be modified!!!
    name = ""             ## A custom name for the file
    file_name = "XX.wav"  ## SD-Card-Format Filename of the file
    index = ""

    def __init__(self, path, file_name):
        self.path = path
        self.file_name = file_name
        print(path)
        self.name = os.path.basename(path)
        return super().__init__()

    def copy_file_to_card(self):
        dest_folder = Globals.SD_CARD_PATH
        if len(dest_folder) <= 4 and dest_folder != self.path:               #if path is 4 characters, e.g. "G:\\" and not copying to same directory
            shutil.copy(self.path, dest_folder + self.file_name)



