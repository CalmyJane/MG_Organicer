from CanvasButton import CanvasButton
from CanvasButton import SwitchModes

class ButtonBar(object):
    """Holds several MgButtons and aligns them in a row. also displays the settings-parameter spread on the different LEDs"""
    buttons = [] ## 6 MgButtons
    x=0 ##x-position
    y=0 ##y-position
    root = 0
    canvas = 0
    spacing = 114

    current_btn = 0

    new_slot_callback = 0 ## is called when a new slot is selected

    def __init__(self, *args, **kwargs):
        self.canvas=kwargs.pop('canvas')
        self.root=kwargs.pop('root')
        self.x=kwargs.pop('x')
        self.y=kwargs.pop('y')
        self.init_buttons()
        return super().__init__(*args, **kwargs)

    def init_buttons(self):
        self.buttons = []
        for i in range(6):
            btn = CanvasButton(canvas=self.canvas, root=self.root, x=self.x+self.spacing*i, y=self.y, label="Button"+str(i), switch_mode=SwitchModes.switch_when_released)
            btn.value_change_callback=self.btn_value_change
            self.buttons.append(btn)
        self.buttons[0].set_value(True)
        self.current_btn = self.buttons[0]

    def btn_value_change(self, value, btn):
        if btn == self.current_btn:
            btn.set_value(True)
        else:
            self.current_btn.set_value(False)
            self.current_btn = btn
            self.current_btn.set_value(True)
            self.new_slot_callback(self.find_button_index(self.current_btn.label))

    def find_button(self, label):
        for btn in self.buttons:
            if btn.label == label:
                return btn

    def find_button_index(self, label):
        for i, btn in enumerate(self.buttons):
            if btn.label == label:
                return i