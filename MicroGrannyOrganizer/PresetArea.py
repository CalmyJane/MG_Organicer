from Knob import Knob
from Preset import Preset

class PresetArea(object):
    """right side of the screen showing buttons and knobs for editing presets"""
    root = 0            ## TKinter root object
    canvas = 0          ## TKinter Canvas
    knobs = []          ## Contains nobs in order: Attack, Release, Start, End, Rate, Crush, Grain, Shift

    knob_offs_x=880
    knob_offs_y=100
    knob_space_x=160
    knob_space_y=80

    preset = 0 ##contains the currently displayed preset
    active_slot = 0 ##contains the index of the currently selected slot of the preset (0-5)

    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        # Create Knobs
        sizes = (((0,127), (0,127)), ((0,1023), (0,1023)), ((0,1023), (0,127)), ((0,127),(-127,128)))
        names = (("ATTACK", "RELEASE"),("START","END"),("SAMPLE\nRATE","CRUSH"),("GRAIN\nSIZE","SHIFT\nSPEED"))
        tags = (("Attack", "Release"),("Start","End"),("Rate","Crush"),("Loop_Length","Shift_Speed"))
        self.knobs = []
        for y, pair in enumerate(sizes):
            for x, size in enumerate(pair):
                cor_x = self.knob_offs_x + x*self.knob_space_x
                cor_y = self.knob_offs_y + y*self.knob_space_y
                knob = Knob(self.root, self.canvas, cor_x, cor_y, size[0], size[1], names[y][x])
                knob.tag=tags[y][x]
                knob.new_value_callback = self.value_update
                self.knobs.append(knob)
        return super().__init__()

    def display_preset(self, preset):
        self.preset=preset
        self.active_slot = 0
        self.display_slot(0, preset)

    def value_update(self, tag, value):
        ## new value from knob, update preset-object with new value
        self.preset.slots[self.active_slot][self.preset.get_name_index(tag)] = value

    def display_slot(self, index, preset):
        self.knobs[0].set_value(preset.slots[index][self.preset.get_name_index("Attack")])
        self.knobs[1].set_value(preset.slots[index][self.preset.get_name_index("Release")])
        self.knobs[2].set_value(preset.slots[index][self.preset.get_name_index("Start")])
        self.knobs[3].set_value(preset.slots[index][self.preset.get_name_index("End")])
        self.knobs[4].set_value(preset.slots[index][self.preset.get_name_index("Rate")])
        self.knobs[5].set_value(preset.slots[index][self.preset.get_name_index("Crush")])
        self.knobs[6].set_value(preset.slots[index][self.preset.get_name_index("Loop_Length")])
        self.knobs[7].set_value(preset.slots[index][self.preset.get_name_index("Shift_Speed")])