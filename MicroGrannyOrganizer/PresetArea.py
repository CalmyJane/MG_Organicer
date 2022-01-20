from Knob import Knob
from Preset import Preset
from CanvasButton import CanvasButton
from CanvasButton import SwitchModes
from ButtonBar import ButtonBar
from SettingsBar import SettingsBar
from KnobButton import KnobButton

class PresetArea(object):
    """right side of the screen showing buttons and knobs for editing presets"""
    root = 0            ## TKinter root object
    canvas = 0          ## TKinter Canvas
    file_list = 0       ## List of all files, presets and samples
    knobs = []          ## Contains nobs in order: Attack, Release, Start, End, Rate, Crush, Grain, Shift

    knob_offs_x=780
    knob_offs_y=110
    knob_space_x=90
    knob_space_y=110

    preset = 0 ##contains the currently displayed preset
    active_slot = 0 ##contains the index of the currently selected slot of the preset (0-5)
    button_bar = 0 ##stores the buttonbar object containing knobs and BIGBUTTONS
    settings_bar = 0 ## the leds to toggle the 5 boolean settings

    def __init__(self, root, canvas, file_list):
        self.file_list=file_list
        self.root = root
        self.canvas = canvas
        # Create Knobs
        sizes = ((0,126), (0,126), (0,1022), (0,1022), (0,1022), (0,126), (0,126),(-127,127))
        names = ("ATTACK", "RELEASE","START","END","RATE","CRUSH","GRAIN","SHIFT")
        tags = ("Attack", "Release","Start","End","Rate","Crush","Loop_Length","Shift_Speed")
        self.knobs = []
        rows=4
        cols=2
        for y in range(cols):
            for x in range(rows):
                cor_x = self.knob_offs_x + x*self.knob_space_x
                cor_y = self.knob_offs_y + y*self.knob_space_y

                knob = KnobButton(min=sizes[y*rows+x][0],
                                max=sizes[y*rows+x][1],
                                label=names[y*rows+x],
                                x=cor_x,
                                y=cor_y,
                                root=self.root,
                                canvas=self.canvas,
                                width=90,
                                height=90,
                                on_img='images\\knob_on.png',
                                off_img='images\\knob_off.png',
                                disabled_img='images\\knob_dis.png',
                                highlight_img='images\\knob_high.png',
                                label_dock='down',
                                label_font='Courier 14 bold')
                knob.tag=tags[y*rows+x]
                knob.new_value_callback = self.value_update
                self.knobs.append(knob)

        self.button_bar = ButtonBar(canvas = self.canvas, root=self.root, file_list = self.file_list, x=459, y=497)
        self.button_bar.new_slot_callback = self.new_slot_selected
        self.button_bar.retrigger_callback = self.button_bar_retriggered
        self.button_bar.data_dropped_callback = self.assign_sample
        self.settings_bar = SettingsBar(canvas = self.canvas, root=self.root, x=459, y=415)
        self.settings_bar.new_setting_callback = self.new_setting
        return super().__init__()

    def assign_sample(self, sample, index):
        self.preset.set_param(index, 'Name', sample.file_name.split('.')[0].upper())
        self.new_slot_selected(index)

    def new_slot_selected(self, index):
        ## called when new slot is selected via one of the 6 buttons
        self.active_slot = index
        self.display_slot(index, self.preset)
        ##select sample in sample view
        if self.preset:
            self.root.sample_tree.select_file(self.preset.get_param(index, 'Name')+'.wav')

    def button_bar_retriggered(self, index):
        self.root.sample_tree.select_file(self.preset.get_param(index, 'Name')+'.wav')

    def new_setting(self, setting):
        ## called when setting bar was changed
        was_tuned = self.preset.get_setting(self.active_slot, "TUNED")
        self.value_update("Setting", setting)
        if not self.preset.get_setting(self.active_slot, "TUNED") == was_tuned:
            self.update_rate_knob(self.active_slot, self.preset)

    def display_preset(self, preset):
        self.preset=preset
        self.active_slot = 0
        self.display_slot(0, preset)

    def value_update(self, tag, value):
        ## new value from knob, update preset-object with new value
        if self.preset:
            if tag=="Rate":
                if self.preset.get_setting(self.active_slot, "TUNED"):
                    value = round((value+36)/42*1022)
                else:
                    value = round((value+360)/420*1022)
            self.preset.slots[self.active_slot][self.preset.get_name_index(tag)] = value

    def display_slot(self, index, preset):
        if preset:
            self.button_bar.set_labels(self.preset)
            self.button_bar.set_slot(index)
            self.knobs[0].set_num_value(preset.slots[index][self.preset.get_name_index("Attack")])
            self.knobs[1].set_num_value(preset.slots[index][self.preset.get_name_index("Release")])
            self.knobs[2].set_num_value(preset.slots[index][self.preset.get_name_index("Start")])
            self.knobs[3].set_num_value(preset.slots[index][self.preset.get_name_index("End")])
            self.update_rate_knob(index, preset)
            self.knobs[5].set_num_value(preset.slots[index][self.preset.get_name_index("Crush")])
            self.knobs[6].set_num_value(preset.slots[index][self.preset.get_name_index("Loop_Length")])
            self.knobs[7].set_num_value(preset.slots[index][self.preset.get_name_index("Shift_Speed")])
            self.settings_bar.set_setting(preset.slots[index][self.preset.get_name_index("Setting")])

    def update_rate_knob(self, index, preset):
        ## sets the rate-knob
        ## if tuned-setting=true -> Scale -36 to 6, with -36=0 and 6=1022
        ## if tuned-setting=false -> Scale -360 to 60, with -360=0 and 60=1022
        if preset.get_setting(index, "TUNED"):
            max = 6
            min = -36
            value = round(preset.get_param(index, "Rate")/1022 * 42 - 36)
        else:
            max = 60
            min = -360
            value = round(preset.get_param(index, "Rate")/1022 * 420 - 360)
        self.knobs[4].min = min
        self.knobs[4].max = max
        self.knobs[4].set_num_value(value)

    def redraw(self):
        self.display_slot(self.button_bar.get_slot_index(), self.preset)