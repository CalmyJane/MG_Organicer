import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import *
from tkinter.ttk import *
import PIL
from PIL import Image
from PIL import ImageTk
from PIL import *
from enum import Enum

class SwitchModes(Enum):
    switch_when_pressed = 0
    switch_when_released = 1
    switch_until_released = 2
    no_operation = 3

class CanvasButton(object):
    """a tkinter UI-Object that represents a button on a canvas. Has benefits, since the button does not need to be square"""

    ##Variable syntax:
    ##i = 'image' -> ion_img=image-object for the on-image
    ##c = 'canvas' -> cimg=canvas-image-object for the current image
    ##tk= 'TKimage' -> tkon_img=tk-image-object for on state

    x=0 ## x-position
    y=0 ## y-position
    label="Button0" ## name of the button
    on_img='images\\button_on.png' ## image in on-state
    off_img='images\\button_off.png' ## image in off-state
    dis_img='images\\button_disabled.png' ## image in disabled-state
    high_img='images\\button_highlight.png' ## image in highlight-state
    ion_img=0 ## image object in on-state
    ioff_img=0 ## image object in off-state
    idis_img=0 ## image object in disabled-state
    ihigh_img=0 ## image object in highlight-state
    tkon_img=0 ## TKImage Object on-state
    tkoff_img=0 ## TKImage Object in off-state
    tkdis_img=0 ## TKImage Object in disabled-state
    tkhigh_img=0 ## TKImage Object in highlight-state
    cimg=0 ## currently displayed image
    chigh=0 ## highlight-image, overlays cimg
    switch_mode = SwitchModes.switch_until_released
    width = 100 ## width of the image
    height = 100 ## height of the image

    label_font = ('Courier 12 bold') ## font of the label
    clabel = 0 ## contains the canvas text-object for label
    label_visible = True ## is the label drawn
    label_offs_x = 0
    label_offs_y = 0

    value=False ## current value of the button
    value_change_callback = 0 ## function to be called on valuechange, must accept
    clicked_callback = 0 ## function to be called on mousedown on the button
    canvas:Canvas = 0 ## canvas to draw the button on (required)
    root:tk = 0 ## the root app-object

    clicked = False ## stores if button was clicked to use switch when released on mouseup
    outside = False ## info if cursor was dragged out of button after click
    disabled = False ## is the button clickable or not
    highlighted = False ## is the button highlight-image visible

    def __init__(self, *args, **kwargs):
        ## get tags
        self.canvas = kwargs.pop('canvas') ##canvas is required, throws error if not passed
        self.root = kwargs.pop('root') ##canvas is required, throws error if not passed

        if kwargs.get('on_img'):
            self.on_img = kwargs.pop('on_img')
        if kwargs.get('off_img'):
            self.off_img = kwargs.pop('off_img')
        if kwargs.get('disabled_img'):
            self.dis_img = kwargs.pop('disabled_img')
        if kwargs.get('highlight_img'):
            self.high_img = kwargs.pop('highlight_img')
        if kwargs.get('command'):
            self.value_change_callback = kwargs.pop('command')
        if kwargs.get('x'):
            self.x = kwargs.pop('x')
        if kwargs.get('y'):
            self.y = kwargs.pop('y')
        if kwargs.get('width'):
            self.width = kwargs.pop('width')
        if kwargs.get('height'):
            self.height = kwargs.pop('height')
        if not kwargs.get('label')==None:
            self.label = kwargs.pop('label')
        if kwargs.get('label_font'):
            self.label_font = kwargs.pop('label_font')
        if not kwargs.get('label_visible') == None:
            self.label_visible = kwargs.pop('label_visible')
        if kwargs.get('switch_mode'):
            self.switch_mode = kwargs.pop('switch_mode')
        if kwargs.get('label_offs_x'):
            self.label_offs_x = kwargs.pop('label_offs_x')
        if kwargs.get('label_offs_y'):
            self.label_offs_y = kwargs.pop('label_offs_y')
        self.value_change_callback = self.default_callback
        self.clicked_callback = self.default_callback
        print(kwargs)
        ## register events
        self.root.binder.bind('<ButtonPress-1>', self.mDown) 
        self.root.binder.bind('<ButtonRelease-1>', self.mUp) 
        self.root.binder.bind('<B1-Motion>', self.lmMove) 
        self.root.binder.bind('<Motion>', self.mMove) 
        ##create button
        self.create_button()
        ##Draw Label
        if self.label_visible:
            self.draw_label()
        ## call parent 
        return super().__init__(*args, **kwargs)

    def create_button(self):
        self.ion_img = Image.open(self.on_img).resize((self.width, self.height), Image.ANTIALIAS)
        self.ioff_img = Image.open(self.off_img).resize((self.width, self.height), Image.ANTIALIAS)
        self.idis_img = Image.open(self.dis_img).resize((self.width, self.height), Image.ANTIALIAS)
        self.ihigh_img = Image.open(self.high_img).resize((self.width, self.height), Image.ANTIALIAS)
        self.tkon_img=ImageTk.PhotoImage(self.ion_img)
        self.tkoff_img=ImageTk.PhotoImage(self.ioff_img)
        self.tkdis_img=ImageTk.PhotoImage(self.idis_img)
        self.tkhigh_img=ImageTk.PhotoImage(self.ihigh_img)
        self.cimg=self.canvas.create_image(self.x, self.y, image=self.tkoff_img)

    ## Event Callbacks
    def mUp(self, event):
        if self.clicked:
            bbox = self.canvas.bbox(self.cimg)
            if self.switch_mode == SwitchModes.switch_until_released:
                self.switch_off()
            elif self.switch_mode == SwitchModes.switch_when_released:
                if bbox[0] < event.x < bbox[2] and bbox[1] < event.y < bbox[3]:
                    self.toggle() ##if released inside button and was clicked before, toggle on release
            self.clicked = False

    def mDown(self, event):
        bbox = self.canvas.bbox(self.cimg)
        if bbox[0] < event.x < bbox[2] and bbox[1] < event.y < bbox[3] and not self.disabled:
            # click inside button and button not disabled
            self.clicked = True
            if self.switch_mode == SwitchModes.switch_until_released:
                self.switch_on()
            elif self.switch_mode == SwitchModes.switch_when_pressed:
                self.toggle()
        self.clicked_callback(self.value, self)

    def mMove(self, event):
        #on every move of the mouse
        bbox = self.canvas.bbox(self.cimg)
        inside = bbox[0] < event.x < bbox[2] and bbox[1] < event.y < bbox[3]
        if inside and not self.disabled:
            self.show_highlight(True)
        else:
            self.show_highlight(False)

    def lmMove(self, event):
        #on every move while left mouse is clicked
        bbox = self.canvas.bbox(self.cimg)
        inside = bbox[0] < event.x < bbox[2] and bbox[1] < event.y < bbox[3]
        if self.clicked:
            if self.switch_mode == SwitchModes.switch_until_released:
                # if switch until released, track if curser moves out and back in again, and toggle button accordingly
                bbox = self.canvas.bbox(self.cimg)
                if not inside:
                    if not self.outside:
                        # just moved outside button button area
                        self.outside = True
                        if self.switch_mode == SwitchModes.switch_until_released:
                            self.switch_off()
                        elif self.switch_mode == SwitchModes.switch_when_released:
                            self.toggle()
                else:
                    # moved inside box
                    if self.outside:
                        #moved back inside
                        self.switch_on()
                        self.outside = False

    def show_highlight(self, show):
        self.highlighted = show
        if show:
            self.canvas.delete(self.chigh)
            self.chigh = self.canvas.create_image(self.x, self.y, image=self.tkhigh_img)
        else:
            self.canvas.delete(self.chigh)
        if self.label_visible:
            self.draw_label()
    
    def toggle(self):
        if self.value:
            self.switch_off()
        else:
            self.switch_on()

    def switch_on(self):
        last_val=self.value
        self.set_value(True)
        if not last_val and not self.outside:
            self.value_change()

    def switch_off(self):
        last_val = self.value
        self.set_value(False)
        if last_val and not self.outside:
            self.value_change()

    def set_value(self, value):
        self.value = value
        self.redraw()

    def value_change(self):
        self.value_change_callback(self.value, self)

    def default_callback(self, value, label):
        pass ##do nothing

    def set_disabled(self, disabled):
        self.disabled = disabled
        if disabled:
            img = self.cimg
            self.cimg = self.canvas.create_image(self.x, self.y, image=self.tkdis_img)
            self.canvas.delete(img)
        else:
            set_value(self.value)

    def redraw(self):
        img = self.cimg
        if self.value:
            image = self.tkon_img
        else:
            image = self.tkoff_img
        self.cimg = self.canvas.create_image(self.x, self.y, image=image)
        self.canvas.delete(img)
        if self.highlighted:
            self.show_highlight(True)
        if self.label_visible:
            self.draw_label()

    def draw_label(self):
        self.canvas.delete(self.clabel)
        self.clabel=self.canvas.create_text(self.x+self.label_offs_x, self.y+self.label_offs_y, text=self.label, fill="silver", font=self.label_font, justify=CENTER)
