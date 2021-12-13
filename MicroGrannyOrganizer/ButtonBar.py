from MgButton import MgButton

class ButtonBar(object):
    """Holds several MgButtons and aligns them in a row. also displays the settings-parameter spread on the different LEDs"""
    buttons = [] ## 6 MgButtons
    x=0 ##x-position
    y=0 ##y-position
    root = 0
    canvas = 0

    def __init__(self, *args, **kwargs):
        self.canvas=kwargs.pop('canvas')
        self.root=kwargs.pop('root')
        self.x=kwargs.pop('x')
        self.y=kwargs.pop('y')
        self.init_buttons()
        return super().__init__(*args, **kwargs)

    def init_buttons(self):
        button = MgButton(root=self.root, canvas=self.canvas, x=self.x, y=self.y)