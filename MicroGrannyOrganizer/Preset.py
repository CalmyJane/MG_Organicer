from collections import namedtuple 
import os
from CardFile import CardFile
import Globals


class Preset(CardFile):
    """Stores decoded data of a preset file and reads/parses/writes the preset file"""

    ## Preset-Files are memory-dumps from the MicroGranny containing several Variables
    ## Each variable can be between 1 and 10 bits
    ## The class reads the file and stores a boolean array with all bits
    ## Via get_var() and set_var() the variables in the bitstream can be modified
    ## This code rebuilds (more or less) the code found here:
    ## https://github.com/bastl-instruments/bastlMicroGranny/blob/master/examples/microGranny2_5/MEM.ino

    ## Variable Description:
    ## Num Length Description
    ## #0  - 10 - Rate
    ## #1  - 7  - Crush
    ## #2  - 7  - Attack
    ## #3  - 7  - Release
    ## #4  - 7  - Loop Length
    ## #5  - 8  - Shift Speed
    ## #6  - 10 - Start
    ## #7  - 10 - End
    ## #8  - 8  - Setting
    ## #9  - 7  - Filename Character 1 - Ascii value
    ## #10 - 7  - Filename Character 2 - Ascii value

    Slot = namedtuple('slot', ['Name', 'Rate', 'Crush', 'Attack', 'Release', 'Loop_Length', 'Shift_Speed', 'Start', 'End', 'Setting'])  ##stores the data for one slot of the preset, 
    slots = []
    bitstream = []

    VARIABLE_NAMES = ["Name", "Rate", "Crush", "Attack", "Release", "Loop Length", "Shift Speed", "Start", "End", "Setting"]
    ## Length of each variable as found in the microgranny sourcecode
    VARIABLE_LENGTHS = (10,7,7,7,7,8,10,10,8,7,7) #the length of each variable stored in the bitstream. 88bits used in total, bitstream is a bit longer

    def __init__(self, path, file_name):
        self.read_file(path)
        self.read_params()
        return super().__init__(path, file_name)

    def read_params(self):
        ## reads the parameters from the bitstream and updates the slots-tuples
        ## you should call read_file() before calling this!
        self.slots = []
        #print("")
        #print("New Variable Values:")
        #print("")
        for slot in range(6):
            #convert each 12 bytes to bitstream for one slot
            debugstr = ""
            sname = chr(self.get_var(slot, 9)) + chr(self.get_var(slot, 10))
            srate = self.get_var(slot, 0)
            scrush = self.get_var(slot, 1)
            sattack = self.get_var(slot, 2)
            srelease = self.get_var(slot, 3)
            slooplength = self.get_var(slot, 4)
            sshiftspeed = self.get_var(slot, 5)
            sstart = self.get_var(slot, 6)
            send = self.get_var(slot, 7)
            ssetting = self.get_var(slot, 8)
            slot_tuple = self.Slot(sname, srate, scrush, sattack, srelease, slooplength, sshiftspeed, sstart, send, ssetting)
            self.slots.append(slot_tuple)

        #    for var in range(11):
        #        debugstr += str(self.get_var(slot, var)).zfill(4)
        #        debugstr += " - "
        #    print(debugstr)
        #print("")

        

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

    def write_file_to_card(self):
        #writes the bitstream to a preset file
        bytes = []
        for n in range(int(len(self.bitstream)/8)):
            byte = self.bits_to_number(self.bitstream[n*8:(n+1)*8])
            bytes.append(byte)
        file = open(Globals.SD_CARD_PATH + self.file_name, "wb")
        file.flush()
        for byte in bytes:
            file.write(byte.to_bytes(1, 'big'))
        file.close
        #print("")
        #print("Bytes Written:")
        #print(bytes)
        #print("")

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
