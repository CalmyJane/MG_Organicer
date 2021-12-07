import os

class Sample(object):
    """Includes all information about a single sample from the MicroGranny SD Card"""
    filename = "XX.wav"         #filename of the sample as found to the SD-Card
    name = "Default Sample"     #custom name to identify the sample. is stored in seperate file to reload next time you use the card
    path = ""                   #Path on disk only contains path when added through tool and not written yet
    id = ""                     #Unique ID


    def __init__(self, id, name, filename, path):
        self.id = id
        self.name = name
        self.filename = filename
        self.path = path
        self.parse_bits(bits)
        return super().__init__()

    def play(self):
        ## Play the sample through main speaker
        Print("---TO BE DONE---: Playing sample")

    def stop(self):
        ## Stop playing the sample
        Print("---TO BE DONE---: Stop playing sample")

    def write_file(self, path):
        ## Write sample to specified folder, overwrite if exists
        Print("---TO BE DONE---: Write Sample to Card")
