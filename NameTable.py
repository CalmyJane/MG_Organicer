from collections import namedtuple 
import os
from CardFile import CardFile
import json
import Globals

class NameTable(CardFile):
    """Reads/Writes/Creates the NameTable.txt file on the SD-Card. This file stores meta-data of all sample-files, like a custom name"""
    config_lines = []           #contains the lines of the config file
    sample_sets = []                           

    def __init__(self, path):
        ##Read Nametable and fill sample_set
        if not len(path) == 0:
            self.read_name_table(path)
        return super().__init__(path)

    def read_name_table(self, path):
        print(path)
        if os.path.exists(path):
            file = open(path, "r", encoding="utf-8")
            content = file.readlines(-1)
            file.close
            config_lines = []
            for line in content:
                if not len(line) == 0:
                    self.config_lines.append(json.loads(line, object_hook=self.line_decoder))

    def line_decoder(self, line_dict):
        return namedtuple('file_config', line_dict.keys())(*line_dict.values())

    def write_name_table(self):
        file = open(Globals.SD_CARD_PATH + "NameTable.txt", "w", encoding = "utf-8")
        lines = []
        file.flush()
        for line in self.config_lines:
            print(line)
            lines.append(json.dumps(line._asdict()) + "\n")
        file.writelines(lines)
        file.close()

    def add_file(self, file_name, index):
        for line in self.config_lines:
            if line.file_name.lower() == file_name.lower():
                return ##already exists
        self.config_lines.append(CardFile.FileConfig(index, "", file_name))

    def get_file_name(self, custom_name):
        for line in self.config_lines:
            if line.name == custom_name:
                return line.file_name

    def get_custom_name(self, file_name):
        for line in self.config_lines:
            if line.file_name.lower() == file_name.lower():
                return line.name

    def get_index(self, file_name):
        for line in self.config_lines:
            if line.file_name.lower() == file_name.lower():
                return line.index

    def set_name(self, file_name, new_name):
        for line in self.config_lines:
            if line.file_name.lower() == file_name.lower():
                print(line.file_name)
                line.name = new_name



