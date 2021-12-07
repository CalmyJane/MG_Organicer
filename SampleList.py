class SampleList(object):
    """This class parses the SD-Card for wav-files that follow pattern XX.wav, matches them with the NameTable-File and creates Sample-Objects and manages them"""
    samples = []
    sc_path = "G:\\"

    def __init__(self, path):
        self.sc_path = path
        return super().__init__()

    def read_card(self):
        ## Read all wav-files from disk and create new objects
        Print("---TO BE DONE---: Listing Wav-Files")

    def add_samples(self, paths):
        ## Add the new sample to the list
        Print("---TO BE DONE---: Adding Samples")

    def remove_by_name(self, name):
        ## Remove a sample by name
        Print("---TO BE DONE---: Removing by name")

    def remove_by_index(self, index):
        ## Remove a sample by name
        Print("---TO BE DONE---: Removing by index")
        
    def remove_by_index(self, index):
        ## Remove a sample by name
        Print("---TO BE DONE---: Removing by index")



