from Knob import Knob

class PresetArea(object):
    """right side of the screen showing buttons and knobs for editing presets"""
    root = 0            ## TKinter root object
    canvas = 0          ## TKinter Canvas
    knob_atk = 0        ## Knob: Attack
    knob_rel = 0        ## Knob: Release
    knob_start = 0      ## Knob: Start position
    knob_stop = 0       ## Knob: Stop position
    knob_rate = 0       ## Knob: Playback-rate
    knob_crush = 0       ## Knob: Crush
    knob_llength = 0       ## Knob: loop length
    knob_sspeed = 0       ## Knob: shift speed

    knob_offs_x=880
    knob_offs_y=100
    knob_space_x=160
    knob_space_y=80

    preset_list = 0     ##contains the list of presets

    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        # Create Knobs
        knobs = ((self.knob_atk, self.knob_rel), (self.knob_start, self.knob_stop), (self.knob_rate, self.knob_crush), (self.knob_llength, self.knob_sspeed))
        sizes = (((0,127), (0,127)), ((0,1023), (0,1023)), ((0,1023), (0,127)), ((0,127),(-127,128)))
        names = (("ATTACK", "RELEASE"),("START","STOP"),("SAMPLE\nRATE","CRUSH"),("GRAIN\nSIZE","SHIFT\nSPEED"))
        for y, pair in enumerate(knobs):
            for x, knob in enumerate(pair):
                cor_x = self.knob_offs_x + x*self.knob_space_x
                cor_y = self.knob_offs_y + y*self.knob_space_y
                knob = Knob(self.root, self.canvas, cor_x, cor_y, sizes[y][x][0], sizes[y][x][1], names[y][x])

        # Create Preset-List




        return super().__init__()
