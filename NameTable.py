from collections import namedtuple 
import os

class NameTable(object):
    """Reads/Writes/Creates the NameTable.txt file on the SD-Card. This file stores meta-data of all sample-files, like a custom name"""
    Sample_Metadata = namedtuple('slot', ['filename', 'name', 'id']) #contains metadata for a samplefile
    sample_sets = []

    def __init__(self, path):
        ##Read Nametable and fill sample_set
        return super().__init__()


