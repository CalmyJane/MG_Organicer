from CanvasButton import CanvasButton
from CanvasButton import SwitchModes

class SettingsBar(object):
    """contains led-buttons for the 5/6 settings-LEDs, last LED is unused"""

    buttons = [] ## 6 Led MgButtons
    x=0 ##x-position
    y=0 ##y-position
    root = 0
    canvas = 0
    spacing = 114

    current_btn = 0
    current_setting = 0 ## int that contains the bits of the setting, from LSB->Tuned, Legato, Repeat, Sync, Random Shift

    new_setting_callback = 0 ## is called when a new slot is selected

    def __init__(self, *args, **kwargs):
        self.canvas=kwargs.pop('canvas')
        self.root=kwargs.pop('root')
        self.x=kwargs.pop('x')
        self.y=kwargs.pop('y')
        self.init_buttons()
        return super().__init__(*args, **kwargs)

    def init_buttons(self):
        names=('TUNED', 'LEGATO','REPEAT','SYNC','RANDOM SHIFT','')
        self.buttons = []
        for i in range(6):
            btn = CanvasButton(canvas=self.canvas,
                               root=self.root,
                               x=self.x+self.spacing*i,
                               y=self.y,
                               label=names[i],
                               switch_mode=SwitchModes.switch_when_released,
                               width=45,
                               height=45,
                               on_img='images\\setting_on.png',
                               off_img='images\\setting_off.png',
                               disabled_img='images\\setting_disabled.png',
                               highlight_img='images\\setting_highlight.png',
                               label_visible=not i==6,
                               label_offs_y=145)
            btn.value_change_callback=self.btn_value_change
            self.buttons.append(btn)
        self.buttons[5].set_disabled(True)
        self.current_btn = self.buttons[0]

    def btn_value_change(self, value, btn):
        bits = [0,0,0,0,0,0,0,0]

        for i, button in enumerate(self.buttons):
            bits[i] = int(button.value)
        bits.reverse()
        val = 0
        for bit in bits:
            val = (val << 1) | bit
        self.current_setting=val
        self.new_setting_callback(self.current_setting)

    def find_button(self, label):
        for btn in self.buttons:
            if btn.label == label:
                return btn

    def find_button_index(self, label):
        for i, btn in enumerate(self.buttons):
            if btn.label == label:
                return i

    def set_setting(self, setting):
        print(setting)
        bits = ([True if setting & (1 << (7-n)) else False for n in range(8)])[::-1]
        for i, bit in enumerate(bits):
            if i <= 4:
                self.buttons[i].set_value(bit)