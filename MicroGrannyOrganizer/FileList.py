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
    removed_files = []     ##contains samples that are removed, will be removed from card when calling write_to_card()
    name_table = 0           ##contains lookuptable
    undoer = 0               ##contains undo-object

    def __init__(self):
        self.name_table = NameTable(Globals.SD_CARD_PATH + "NameTable.txt", "NameTable.txt")
        self.read_card()
        return super().__init__()

    def read_card(self):
        self.samples = []
        self.presets = []
        self.removed_files = []
        self.name_table.reset()
        ## Read all wav-files from disk and create new objects
        for filename in os.listdir(Globals.SD_CARD_PATH):
            path = Globals.SD_CARD_PATH + filename
            self.import_file(path)
        self.update_custom_names()
        self.samples.sort(key=Sample.get_index)
        if len(self.presets)<=0:
            self.presets.append(Preset("", 'P01.txt'))
        self.update_indexes()

    def import_file(self, path):
        if path.lower().endswith(".wav"):
            ## Sample-File
            self.samples.append(Sample(path, os.path.basename(path)))
        if path.lower().endswith(".txt"):
            if len(os.path.basename(path)) == 7:
                ## Preset-File
                self.presets.append(Preset(path, os.path.basename(path)))
            elif os.path.basename(path) == "NameTable.txt":
                ## NameTable-File
                self.name_table = NameTable(path, "NameTable.txt")
        if self.name_table == 0:
            self.name_table = NameTable(Globals.SD_CARD_PATH + "NameTable.txt", "NameTable.txt")
    
    def update_custom_names(self):
        #updates custom names and indexes of all files with values from NameTable
        for i, sample in enumerate(self.samples):
            index=self.name_table.get_index(sample.file_name)
            if index == None:
                index = 100000
            sample.index = index
            name = self.name_table.get_custom_name(sample.file_name)
            if not name:
                name=""
            sample.name = name

        for i, preset in enumerate(self.presets):
            index=self.name_table.get_index(preset.file_name)
            if index == None:
                index = 100000
            preset.index = index
            name = self.name_table.get_custom_name(preset.file_name)
            if not name:
                name=""
            preset.name = name

        self.update_name_table()

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
        file = self.get_file_by_name(file_name)
        if file:
            if self.is_sample(file_name):
                #remove sample
                self.samples.remove(file)
                if file.is_on_card():
                    self.removed_files.append(file)
            if not self.is_sample(file_name):
                #remove preset
                self.presets.remove(file)
                if file.is_on_card():
                    self.removed_files.append(file)
            #else:
            #    self.presets.remove(self.get_file_by_name(file_name))
            self.update_indexes()

    def write_to_card(self):
        print(self.presets[0].get_param(0, 'Setting'))
        self.update_name_table()
        for rsample in self.removed_files:
            rsample.delete_from_card()
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
        fnums = ('0','1','2','3','4','5','6','7','8','9')
        snums = ('1','2','3','4','5','6')
        for first_char in fnums:
            for second_char in snums:
                fname = "P"+first_char+second_char+".txt"
                if not self.get_file_by_name(fname) and not fname == "P01.txt":
                    return fname

    def insert_sample(self, index, sample):
        self.samples.insert(index, sample)
        self.update_indexes()

    def insert_preset(self, index, preset):
        self.presets.insert(index, preset)
        self.update_indexes()

    def update_indexes(self):
        ## updates the indexes of all samples, usually after a sample was added. also updates name_table
        for i, sample in enumerate(self.samples):
            sample.index = i
        for i, preset in enumerate(self.presets):
            preset.index = i
        self.update_name_table()

    def get_num_new_files(self):
        #returns the number or samples that were added from disk
        counter = 0
        for sample in self.samples+self.presets:
            if not sample.is_on_card():
                counter += 1
        return counter

    def update_name_table(self):
        self.name_table.set_all_files(self.samples+self.presets)


class UndoObject(object):
    depth = abs         ## number of undo-steps kept in memory
    buffer = []         ## buffer of undo-elements

    def __init__(self, first_element):
        self.reset(first_element)
        return super().__init__()

    def add(self, element):
        self.buffer.append(element)
        if len(self.buffer) > depth:
            self.buffer = self.buffer[END-depth+1:END]

    def undo(self):
        element = self.buffer[END]
        if len(self.buffer)>1:
            self.buffer.remove(element)
        return element

    def reset(self, first_element):
        if first_element:
            self.buffer.append(first_element)