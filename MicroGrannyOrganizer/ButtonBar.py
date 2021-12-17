from CanvasButton import CanvasButton
from CanvasButton import SwitchModes
from Preset import Preset
from FileList import FileList

class ButtonBar(object):
    """Holds several MgButtons and aligns them in a row. also displays the settings-parameter spread on the different LEDs"""
    buttons = [] ## 6 MgButtons
    x=0 ##x-position
    y=0 ##y-position
    root = 0
    canvas = 0
    spacing = 114

    current_btn = 0
    file_list = 0

    new_slot_callback = 0 ## is called when a new slot is selected
    retrigger_callback = 0## is called when a selected button is clicked again to reselect the sample in sample view and retrigger autoplay

    data_dropped_callback = 0 ## is called when one of the buttons has data dragged to it

    def __init__(self, *args, **kwargs):
        self.canvas=kwargs.pop('canvas')
        self.root=kwargs.pop('root')
        self.file_list=kwargs.pop('file_list')
        self.x=kwargs.pop('x')
        self.y=kwargs.pop('y')
        self.init_buttons()
        return super().__init__(*args, **kwargs)

    def init_buttons(self):
        self.buttons = []
        for i in range(6):
            btn = CanvasButton(canvas=self.canvas, 
                               root=self.root, 
                               x=self.x+self.spacing*i, 
                               y=self.y, 
                               label="", 
                               switch_mode=SwitchModes.switch_when_pressed)
            btn.value_change_callback=self.btn_value_change
            btn.data_dropped_callback=self.data_dropped
            self.buttons.append(btn)
        self.buttons[0].set_value(True)
        self.current_btn = self.buttons[0]

    def data_dropped(self, btn, data):
        if self.data_dropped_callback:
            self.data_dropped_callback(data, self.buttons.index(btn)) ## pass dragndrop data and slot-index to caller


    def btn_value_change(self, value, btn):
        if btn == self.current_btn:
            btn.set_value(True)
            self.retrigger_callback(self.buttons.index(btn))
        else:
            self.current_btn.set_value(False)
            self.current_btn = btn
            self.current_btn.set_value(True)
            self.new_slot_callback(self.buttons.index(btn))

    def set_slot(self, slot):
        self.current_btn.set_value(False)
        self.current_btn = self.buttons[slot]
        self.current_btn.set_value(True)

    def set_labels(self, preset:Preset):
        if preset:
            for i, btn in enumerate(self.buttons):
                fname = preset.get_param(i, 'Name')+".wav"
                sample = self.file_list.get_file_by_name(fname)
                if sample:
                    text=sample.file_name
                else:
                    text='<EMPTY>'
                if len(text)==0:
                    text=sample.file_name
                lines = ""
                i=0
                while len(text) >= 8 and i<=3:
                    line=text[:8]+"\n"
                    lines += line
                    text = text[8:len(text)]
                    i+=i
                if len(text)<=8:
                    lines+=text
                btn.label = lines
                btn.redraw()

    def get_slot_index(self):
        return self.buttons.index(self.current_btn)