import os
import shutil
from CardFile import CardFile

class Sample(CardFile):
    """Includes all information about a single sample from the MicroGranny SD Card"""

    def __init__(self, path):
        return super().__init__(path)

    def play(self):
        ## Play the sample through main speaker
        Print("---TO BE DONE---: Playing sample")

    def stop(self):
        ## Stop playing the sample
        Print("---TO BE DONE---: Stop playing sample")

