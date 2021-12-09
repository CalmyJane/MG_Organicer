import os
import Globals
from Preset import Preset
from Sample import Sample
from collections import namedtuple 
from CardFile import CardFile
from NameTable import NameTable
import pathlib


class FileList(object):
    """This class parses the SD-Card for wav-files that follow pattern XX.wav, matches them with the NameTable-File and creates Sample-Objects and manages them"""
    samples = []             ##contains all samples (A0.wav) found on card
    presets = []             ##contains all presets (P01.txt) found on card
    name_table = 0           ##contains lookuptable

    def __init__(self):
        name_table = NameTable(Globals.SD_CARD_PATH + "NameTable.txt", "NameTable.txt")
        self.read_card()
        return super().__init__()

    def read_card(self):
        ## Read all wav-files from disk and create new objects
        for filename in os.listdir(Globals.SD_CARD_PATH):
            path = Globals.SD_CARD_PATH + filename
            print("Read File: " + path)
            self.import_file(path)
        self.update_custom_names()
        

    def import_file(self, path):
        if path.lower().endswith(".wav"):
            ## Sample-File
            self.samples.append(Sample(path, os.path.basename(path)))
        if path.lower().endswith(".txt"):
            if len(os.path.basename(path)) == 7:
                ## Preset-File
                self.presets.append(Preset(path, os.path.basename(path)))
            else:
                ## NameTable-File
                self.name_table = NameTable(path, "NameTable.txt")
        if self.name_table == 0:
            self.name_table = NameTable(Globals.SD_CARD_PATH + "NameTable.txt", "NameTable.txt")
    
    def update_custom_names(self):
        #updates custom names of all files with values from NameTable
        for i, sample in enumerate(self.samples):
            self.name_table.add_file(sample.file_name, i)
            file_name = self.name_table.get_custom_name(sample.file_name)
            if not file_name is None:
                sample.name = self.name_table.get_custom_name(sample.file_name)
                sample.index = self.name_table.get_index(sample.file_name)

        for i, preset in enumerate(self.presets):
            self.name_table.add_file(preset.file_name, i)
            if not self.name_table.get_custom_name(preset.file_name) is None:
                preset.name = self.name_table.get_custom_name(preset.file_name)

    def name_file(self, file_name, name):
        file = self.get_file_by_name(file_name)
        if not file==None:
            file.name = name
            self.name_table.set_name(file_name, name)

    def get_sample_by_name(self, name):
        for sample in self.samples:
            if sample.name == name:
                return sample

    def get_file_by_name(self, file_name):
        for sample in self.samples:
            if sample.file_name.lower() == file_name.lower():
                return sample
        for preset in self.presets:
            if preset.file_name.lower() == file_name.lower():
                return preset

    def get_preset_by_name(self, name):
        for preset in self.presets:
            if preset.name == name:
                return preset

    def get_preset_by_file_name(self, file_name):
        for preset in self.presets:
            if preset.file_name.lower() == file_name.lower():
                return preset

    def get_index(self, name):
        for i, sample in enumerate(self.samples):
            if sample.name == name:
                return i
        return -1 ## Sample not found
    
    def is_sample(self, file_name):
        return pathlib.Path(file_name).suffix.lower() == '.wav'

    def remove_by_name(self, file_name):
        ## Remove a sample by name
        if self.is_sample(file_name):
            self.samples.remove(self.get_file_by_name(file_name))
        else:
            self.presets.remove(self.get_file_by_name(file_name))
        print(len(self.samples))

    def remove_by_index(self, index):
        ## Remove a sample by name
        Print("---TO BE DONE---: Removing by index")
        
    def remove_by_index(self, index):
        ## Remove a sample by name
        Print("---TO BE DONE---: Removing by index")

    def write_to_card(self):
        for sample in self.samples:
            sample.copy_file_to_card()
        for preset in self.presets:
            preset.write_file_to_card()
        self.name_table.write_name_table()

    def get_free_sample_name(self):
        ## returns a Valid sample filename for the microgranny that is not yet taken
        ## Filenames are A0.wav - ZZ.wav
        ## 00.wav - 99.wav are reserved for recorded samples from the MG, they can be edited but not written from PC
        chars = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
        nums = ('0','1','2','3','4','5','6','7','8','9')
        for first_char in chars:
            for second_char in nums + chars:
                fname = first_char+second_char+".wav"
                if not self.get_file_by_name(fname):
                    return fname

    def get_free_preset_name(self):
        ## returns a Valid preset filename for the microgranny that is not yet taken
        ## Filenames are P01.txt - P99.txt
        nums = ('0','1','2','3','4','5','6','7','8','9')
        for first_char in nums:
            for second_char in nums:
                fname = "P"+first_char+second_char+".txt"
                if not self.get_file_by_name(fname) and not fname == "P01.txt":
                    return fname