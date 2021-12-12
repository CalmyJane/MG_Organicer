from collections import namedtuple 
import os
from CardFile import CardFile
import json
import Globals

class ConfigData(object):
    index = 0
    name = ""
    file_name = ""

    def __init__(self, **kw):
        sample=None
        if 'sample' in kw:
            sample = kw.pop('sample')
        if sample:
            self.index = sample.index
            self.name = sample.name
            self.file_name = sample.file_name
        else:
            self.index = kw.pop('index')
            self.name = kw.pop('name')
            self.file_name = kw.pop('file_name')

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
        self.config_lines = [] 
        if not len(path) == 0:
            self.read_name_table(path)
        return super().__init__(path, file_name)

    def reset(self):
        self.config_lines = []

    def read_name_table(self, path):
        ## Reads the NameTable.txt file and decodes the content
        if os.path.exists(path):
            file = open(path, "r", encoding="utf-8")
            content = file.readlines(-1)
            file.close
            self.config_lines = []
            for line in content:
                if not len(line) == 0:
                    config = json.loads(line)
                    if not self.exists(config["file_name"]):
                        ## add new config object to list
                        self.config_lines.insert(config["index"], ConfigData(index=config["index"], name=config["name"], file_name=config["file_name"]))
                    else:
                        ## duplicate entry, replace original. shouldnt happen.
                        self.config_lines[self.get_array_index(config["file_name"])] = ConfigData(index=config["index"], name=config["name"], file_name=config["file_name"])

    def write_name_table(self):
        file = open(Globals.SD_CARD_PATH + "NameTable.txt", "w")
        lines = ""
        file.seek(0)
        for line in self.config_lines:
            lines += line.get_config_string() + "\n"
        file.write(lines)
        file.truncate()
        file.close()

    def add_file(self, file_name, index, name):
        for line in self.config_lines:
            if line.file_name.lower() == file_name.lower():
                return ##already exists
        self.config_lines.append(ConfigData(index=index, name=name, file_name=file_name))

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

    def get_text_table(self):
        out = "Name Table: \n"
        for entry in self.config_lines:
            ind = str(entry.index)
            out += "filename: " + entry.file_name + " - name: " + entry.name + " - index: " + ind + "\n"
        return out

    def set_index(self, file_name, index):
        list_index = self.get_array_index(file_name)
        if list_index:
            self.config_lines[list_index].index = index

    def set_all_files(self, samples):
        self.config_lines = []
        for sample in samples:
            self.config_lines.append(ConfigData(sample=sample))