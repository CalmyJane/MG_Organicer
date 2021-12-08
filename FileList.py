import os
import Globals
from Preset import Preset
from Sample import Sample
from collections import namedtuple 
from CardFile import CardFile
from NameTable import NameTable


class FileList(object):
    """This class parses the SD-Card for wav-files that follow pattern XX.wav, matches them with the NameTable-File and creates Sample-Objects and manages them"""
    samples = []             ##contains all samples (A0.wav) found on card
    presets = []             ##contains all presets (P01.txt) found on card
    name_table = 0           ##contains lookuptable

    def __init__(self):
        name_table = NameTable(Globals.SD_CARD_PATH + "NameTable.txt")
        self.read_card()
        return super().__init__()

    def read_card(self):
        ## Read all wav-files from disk and create new objects
        for filename in os.listdir(Globals.SD_CARD_PATH):
            path = Globals.SD_CARD_PATH + filename
            print("Read Path: " + path)
            self.import_file(path)
        self.update_custom_names()
        

    def import_file(self, path):
        if path.lower().endswith(".wav"):
            ## Sample-File
            self.samples.append(Sample(path))
        if path.lower().endswith(".txt"):
            if len(os.path.basename(path)) == 7:
                ## Preset-File
                self.presets.append(Preset(path))
            else:
                ## NameTable-File
                self.name_table = NameTable(path)
        if self.name_table == 0:
            self.name_table = NameTable(Globals.SD_CARD_PATH + "NameTable.txt")
    
    def update_custom_names(self):
        #updates custom names of all files with values from NameTable
        for i, sample in enumerate(self.samples):
            self.name_table.add_file(sample.file_name, i)
            name = self.name_table.get_custom_name(sample.file_name)
            if not name is None:
                sample.name = self.name_table.get_custom_name(sample.file_name)
        for i, preset in enumerate(self.presets):
            self.name_table.add_file(preset.file_name, i)
            if not self.name_table.get_custom_name(preset.file_name) is None:
                preset.name = self.name_table.get_custom_name(preset.file_name)

    def name_sample(self, file_name, name):
        self.get_sample_by_file_name(file_name).name = name
        print(name)
        self.name_table.set_name(file_name, name)

    def get_sample_by_name(self, name):
        for sample in self.samples:
            if sample.name == name:
                return sample

    def get_sample_by_file_name(self, file_name):
        for sample in self.samples:
            if sample.file_name.lower() == file_name.lower():
                return sample

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

    def remove_by_name(self, name):
        ## Remove a sample by name
        self.samples.remove(self.get_by_name)

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

