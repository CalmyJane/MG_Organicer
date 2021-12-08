import shutil
import os
from collections import namedtuple 
import Globals


class CardFile(object):
    """Abstract class, represents a file on the MicroGrannys SD-Card. Can bei either a Preset ("P01.txt") a Sample ("A0.wav") or NameTable ("NameTable.txt")"""
    FileConfig = namedtuple('file_config', ['id', 'name', 'file_name'])  ## Container for NameTable-data, used to macht filenames to custom names and their index in the list

    path = ""             ## Path without Filename, may be path on Card or path on Drive. Files no computer CAN NOT be modified!!!
    name = ""             ## A custom name for the file
    file_name = "XX.wav"  ## SD-Card-Format Filename of the file

    def __init__(self, path):
        self.path = path
        self.file_name = os.path.basename(path)
        self.name = self.file_name
        return super().__init__()

    def copy_file_to_card(self):
        dest_folder = Globals.SD_CARD_PATH
        if len(dest_folder) <= 4 and dest_folder != self.path:               #if path is 4 characters, e.g. "G:\\" and not copying to same directory
            shutil.copy(self.path, dest_folder + self.file_name)




