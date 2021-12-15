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

class CanvasButton(object):
    """a tkinter UI-Object that represents a button on a canvas. Has benefits, since the button does not need to be square"""

    ##Variable syntax:
    ##i = 'image' -> ion_img=image-object for the on-image
    ##c = 'canvas' -> cimg=canvas-image-object for the current image

    x=0 ## x-position
    y=0 ## y-position
    label="Button0" ## name of the button
    on_img='images\\button_on.png' ## image in on-state
    off_img='images\\button_off.png' ## image in off-state
    ion_img=0 ## image object in on-state
    ioff_img=0 ## image object in off-state
    tkon_img=0 ## TKImage Object on-state
    tkioff_img=0 ## TKImage Object in off-state
    cimg=0 ## image in on-state
    switch_mode = SwitchModes.switch_until_released

    value=False ## current value of the button
    value_change_callback = 0 ## function to be called on valuechange, must accept
    canvas:Canvas = 0 ## canvas to draw the button on (required)
    root:tk = 0 ## the root app-object

    clicked = False ## stores if button was clicked to use switch when released on mouseup
    outside = False ## info if cursor was dragged out of button after click

    def __init__(self, *args, **kwargs):
        ## get tags
        self.canvas = kwargs.pop('canvas') ##canvas is required, throws error if not passed
        self.root = kwargs.pop('root') ##canvas is required, throws error if not passed

        if kwargs.get('on_img'):
            self.off_img = kwargs.pop('off_img')
        if kwargs.get('off_img'):
            self.on_img = kwargs.pop('on_img')
        if kwargs.get('command'):
            self.value_change_callback = kwargs.pop('command')
        if kwargs.get('x'):
            self.x = kwargs.pop('x')
        if kwargs.get('y'):
            self.y = kwargs.pop('y')
        if kwargs.get('label'):
            self.label = kwargs.pop('label')
        if kwargs.get('switch_mode'):
            self.switch_mode = kwargs.pop('switch_mode')
        self.value_change_callback = self.default_callback
        ## register events
        self.root.binder.bind('<ButtonPress-1>', self.mDown) 
        self.root.binder.bind('<ButtonRelease-1>', self.mUp) 
        self.root.binder.bind('<B1-Motion>', self.mMove) 
        ##create button
        self.create_button()
        ## call parent 
        return super().__init__(*args, **kwargs)

    def create_button(self):
        self.ion_img = Image.open(self.on_img).resize((100, 100), Image.ANTIALIAS)
        self.ioff_img = Image.open(self.off_img).resize((100, 100), Image.ANTIALIAS)
        self.tkon_img=ImageTk.PhotoImage(self.ion_img)
        self.tkoff_img=ImageTk.PhotoImage(self.ioff_img)
        self.cimg=self.canvas.create_image(self.x, self.y, image=self.tkoff_img)

    ## Event Callbacks
    def mUp(self, event):
        if self.clicked:
            bbox = self.canvas.bbox(self.cimg)
            if self.switch_mode == SwitchModes.switch_until_released:
                self.set_off()
            elif self.switch_mode == SwitchModes.switch_when_released:
                if bbox[0] < event.x < bbox[2] and bbox[1] < event.y < bbox[3]:
                    self.toggle() ##if released inside button and was clicked before, toggle on release
            self.clicked = False

    def mDown(self, event):
        bbox = self.canvas.bbox(self.cimg)
        if bbox[0] < event.x < bbox[2] and bbox[1] < event.y < bbox[3]:
            # click inside button
            self.clicked = True
            if self.switch_mode == SwitchModes.switch_until_released:
                self.set_on()
            elif self.switch_mode == SwitchModes.switch_when_pressed:
                self.toggle()


    def mMove(self, event):
        if self.clicked:
            if self.switch_mode == SwitchModes.switch_until_released:
                # if switch until released, track if curser moves out and back in again, and toggle button accordingly
                bbox = self.canvas.bbox(self.cimg)
                if not bbox[0] < event.x < bbox[2] or not bbox[1] < event.y < bbox[3]:
                    if not self.outside:
                        # just moved outside button button area
                        self.outside = True
                        if self.switch_mode == SwitchModes.switch_until_released:
                            self.set_off()
                        elif self.switch_mode == SwitchModes.switch_when_released:
                            self.toggle()
                else:
                    # moved inside box
                    if self.outside:
                        #moved back inside
                        self.set_on()
                        self.outside = False

    
    def toggle(self):
        if self.value:
            self.set_off()
        else:
            self.set_on()

    def set_on(self):
        if not self.value and not self.outside:
            self.value_change()
        self.value = True
        img = self.cimg
        self.cimg = self.canvas.create_image(self.x, self.y, image=self.tkon_img)
        self.canvas.delete(img)

    def set_off(self):
        if self.value and not self.outside:
            self.value_change()
        self.value = False
        img = self.cimg
        self.cimg = self.canvas.create_image(self.x, self.y, image=self.tkoff_img)
        self.canvas.delete(img)

    def value_change(self):
        self.value_change_callback(self.value, self.label)

    def default_callback(self, value, label):
        Print('Button clicked, but no Callback assigned in Button: '+self.label)
