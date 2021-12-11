import os
import shutil
from CardFile import CardFile
import winsound

class Sample(CardFile):
    """Includes all information about a single sample from the MicroGranny SD Card"""

    def __init__(self, path, file_name):
        return super().__init__(path, file_name)

    def play(self):
        ## Play the sample through main speaker
        winsound.PlaySound(self.path, winsound.SND_FILENAME and winsound.SND_ASYNC)

    def stop(self):
        ## Stop playing the sample
        Print("---TO BE DONE---: Stop playing sample")

