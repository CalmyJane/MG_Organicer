from collections import namedtuple 
import os


class Preset(object):
    """Stores decoded data of a preset file and reads/parses/writes the preset file"""

    ## Preset-Files are memory-dumps from the MicroGranny containing several Variables
    ## Each variable can be between 1 and 10 bits
    ## The class reads the file and stores a boolean array with all bits
    ## Via get_var() and set_var() the variables in the bitstream can be modified

    ## Variable Description:
    ## Num Length Description
    ## #0  - 10 - ??
    ## #1  - 7  - Attack
    ## #2  - 7  - Release
    ## #3  - 7  - ??
    ## #4  - 7  - ??
    ## #5  - 8  - ??
    ## #6  - 10 - ??
    ## #7  - 10 - ??
    ## #8  - 8  - ??
    ## #9  - 7  - Filename Character 1 - Ascii value
    ## #10 - 7  - Filename Character 2 - Ascii value

    Slot = namedtuple('slot', ['samplename', 'attack', 'release'])  ##stores the data for one slot of the preset, 
    slots = []
    path = "C:\\Temp\\P01.txt"
    filename = "P01.txt"
    name = "Funny Sounds"
    bitstream = []

    ## Variables: ??, ??
    VARIABLE_LENGTHS = (10,7,7,7,7,8,10,10,8,7,7) #the length of each variable stored in the bitstream. 88bits used in total, bitstream is a bit longer

    def __init__(self, path):
        self.path = path
        self.filename = os.path.dirname(path)
        self.read_file(path)
        self.read_params()
        return super().__init__()

    def read_params(self):
        self.slots = []
        for slot in range(6):
            #convert each 12 bytes to bitstream for one slot
            debugstr = ""
            sname = chr(self.get_var(slot, 9)) + chr(self.get_var(slot, 10))
            sattack = self.get_var(slot, 2)
            srelease = self.get_var(slot, 3)

            self.slots.append(self.Slot(sname, sattack, srelease))

            ##DEBUG
            for var in range(11):
                debugstr += str(self.get_var(slot, var))
                debugstr += " - "
            print(debugstr)

    def read_file(self, path):
        ## reads the bitstream from a preset file
        file = open(path,"rb")
        bytes = file.read()
        file.close()
        self.bitstream = []
        int_bytes = []
        for byte in bytes:
            self.bitstream += self.byte_to_bits(byte)
            int_byte = int(byte)
            int_bytes.append(int_byte)
        print(int_bytes)

    def write_file(self, path):
        #writes the bitstream to a preset file
        bytes = []
        for n in range(int(len(self.bitstream)/8)):
            byte = self.bits_to_number(self.bitstream[n*8:(n+1)*8])
            bytes.append(byte)
        print(bytes)

    def byte_to_bits(self, byte): 
        #Convert a byte (int) to an array of booleans representing it's bits
        return self.number_to_bits(byte, 8)

    def number_to_bits(self, number, length):
        #Convert a number to an array of booleans representing it's bits up to the most significant bit used
        return([True if number & (1 << (length-1-n)) else False for n in range(length)])[::-1]

    def bits_to_number(self, bits):
        #Convert a bit (array of bool) to number (int)
        byte = 0
        for i, bit in enumerate(bits):
            if bit:
                byte += 2**(i)
        return(byte)

    def get_var(self, slot_index, var_index):
        #reads a value from the bitstream. analog to the function inside the microgranny sourcecode
        start_bit_rel = 0
        for var_len in self.VARIABLE_LENGTHS[0:(var_index)]:
            #add up all lengths up to variable to get position inside 96-bit preset
            start_bit_rel += var_len
        start_bit = start_bit_rel + slot_index * 96                     #add x*96bits to select current preset
        stop_bit = start_bit + self.VARIABLE_LENGTHS[var_index]
        bits = self.bitstream[start_bit:stop_bit]                       #read variable from bitstream
        return self.bits_to_number(bits)

    def set_var(self, slot_index, var_index, value):
        #sets a variable in the bitstream. analog to the function inside the microgranny sourcecode
        start_bit_rel = 0
        for var_len in self.VARIABLE_LENGTHS[0:(var_index)]:
            #add up all lengths up to variable to get position inside 96-bit preset
            start_bit_rel += var_len
        start_bit = start_bit_rel + slot_index * 96                     #add x*96bits to select current preset
        stop_bit = start_bit + self.VARIABLE_LENGTHS[var_index]
        bits = self.number_to_bits(value, self.VARIABLE_LENGTHS[var_index])
        self.bitstream[start_bit:stop_bit] = bits                       #read variable from bitstream
        return self.bits_to_number(bits)

#preset = Preset("G:\\P01.txt")

