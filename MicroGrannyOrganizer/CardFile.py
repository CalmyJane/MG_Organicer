import shutil
import os
from collections import namedtuple 
import Globals
import json
from pydub import AudioSegment




class CardFile(object):
    """Abstract class, represents a file on the MicroGrannys SD-Card. Can bei either a Preset ("P01.txt") a Sample ("A0.wav") or NameTable ("NameTable.txt")"""

    path = ""             ## Path with Filename, may be path on Card or path on Drive. Files no computer CAN NOT be modified!!!
    name = ""             ## A custom name for the file
    file_name = "XX.wav"  ## SD-Card-Format Filename of the file
    index = "12345"            ## The files index in a list

    def __init__(self, path, file_name):
        self.path = path
        self.file_name = file_name
        self.name = os.path.basename(path)
        return super().__init__()

    def copy_file_to_card(self):
        dest_folder = Globals.SD_CARD_PATH
        if dest_folder + self.file_name != self.path:               #if path is 4 characters, e.g. "G:\\" and not copying to same directory
            shutil.copy(self.path, dest_folder + self.file_name)

    def delete_from_card(self):
        if self.is_on_card():
            os.remove(Globals.SD_CARD_PATH + self.file_name)

    def is_on_card(self):
        ## returns wether this file is placed on the SD-Card or added from disk
        return self.path == Globals.SD_CARD_PATH + self.file_name

    def get_index(self):
        return self.index