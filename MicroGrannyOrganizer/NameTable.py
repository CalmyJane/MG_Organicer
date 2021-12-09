from collections import namedtuple 
import os
from CardFile import CardFile
import json
import Globals

class ConfigData(object):
    index = 0
    name = ""
    file_name = ""

    def __init__(self, index, name, file_name):
        self.index = index
        self.name = name
        self.file_name = file_name

    def get_config_string(self):
        return json.dumps({'index' : self.index, 'name' : self.name, 'file_name' : self.file_name})

    def set_from_string(self, string):
        conf_obj = json.loads(string)
        index = conf_obj["index"]
        name = conf_obj["name"]
        file_name = conf_obj["file_name"]

class NameTable(CardFile):
    """Reads/Writes/Creates the NameTable.txt file on the SD-Card. This file stores meta-data of all sample-files, like a custom name"""
    config_lines = []           #contains the lines of the config file
    sample_sets = []                           

    def __init__(self, path, file_name):
        ##Read Nametable and fill sample_set
        if not len(path) == 0:
            self.read_name_table(path)
        return super().__init__(path, file_name)

    def read_name_table(self, path):
        ## Reads the NameTable.txt file and decodes the content
        if os.path.exists(path):
            file = open(path, "r", encoding="utf-8")
            content = file.readlines(-1)
            file.close
            config_lines = []
            for line in content:
                if not len(line) == 0:
                    config = json.loads(line)
                    if not self.exists(config["file_name"]):
                        ## add new config object to list
                        self.config_lines.insert(config["index"], ConfigData(config["index"], config["name"], config["file_name"]))
                    else:
                        ## duplicate entry, replace original. shouldnt happen.
                        self.config_lines[self.get_array_index(config["file_name"])] = ConfigData(config["index"], config["name"], config["file_name"])



    def write_name_table(self):
        file = open(Globals.SD_CARD_PATH + "NameTable.txt", "w")
        lines = []
        file.seek(0)
        for line in self.config_lines:
            lines.append(line.get_config_string() + "\n")
        file.writelines(lines)
        file.truncate
        file.close()

    def add_file(self, file_name, index):
        for line in self.config_lines:
            if line.file_name.lower() == file_name.lower():
                return ##already exists
        self.config_lines.append(ConfigData(index, "", file_name))

    def get_array_index(self, file_name):
        for i, line in enumerate(self.config_lines):
            if line.file_name == file_name:
                return i       

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

    def set_name(self, file_name, name):
        for line in self.config_lines:
            if line.file_name.lower() == file_name.lower():
                line.name = name

    def exists(self, file_name):
        for line in self.config_lines:
            if line.file_name.lower() == file_name.lower():
                return True
        return False

