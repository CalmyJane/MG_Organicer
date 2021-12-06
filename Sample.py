import os

class Sample(object):
    """Includes all information about a single sample from the MicroGranny SD Card"""
    filename = "XX.wav"         #filename of the sample as found to the SD-Card
    name = "Default Sample"     #custom name to identify the sample. is stored in seperate file to reload next time you use the card
    path = ""                   #Path on disk only contains path when added through tool and not written yet


    def __init__(self, bits):
        self.parse_bits(bits)
        return super().__init__()



    def number_to_bits(self, byte): 
        #Convert a byte (int) to an array of booleans representing it's bits
        return([True if byte & (1 << (7-n)) else False for n in range(8)]) 

    def bits_to_number(self, bits):
        #Convert a bit (array of bool) to byte (int)
        byte = 0
        for i, bit in enumerate(bits):
            if bit:
                byte += 2**(len(bits)-i)
        return(byte)