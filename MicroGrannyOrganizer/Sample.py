import os
import shutil
from CardFile import CardFile
import winsound
import Globals
#from pydub import AudioSegment
#import audiosegment

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

    #def copy_file_to_card(self):
    #    #overwrites the write to card functionality by converting the audiofile
    #    dest_folder = Globals.SD_CARD_PATH
    #    if dest_folder + self.file_name != self.path:               #if path is 4 characters, e.g. "G:\\" and not copying to same directory
    #        audio_file = audiosegment.from_file(self.path).resample(sample_rate_Hz=22050, sample_width=2, channels=1)
    #        audio_file.export(dest_folder + self.file_name, format="wav")
