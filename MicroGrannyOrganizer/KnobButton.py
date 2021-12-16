import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import PIL
from PIL import Image
from PIL import ImageTk
from PIL import *
import numpy
from CanvasButton import CanvasButton

class KnobButton(CanvasButton):
    ## UI Element representing a knob. It consists of an image of a circle, a text indicator in the middle and a label
    ## Value can be changed by scrolling or drag up/down
    ## This object needs a canvas to draw it's elements on

    min = 0    ##min-value for the knob scale
    max = 127  ##max-value for the knob scale
    num_value = 28 ##current value
    pad_angle = 30 ##angle (from bottom of knob) to where scale starts/ends
    offset_angle = 180 ##offset to orient the knob
    speed = 0.5  ##how fast the knob moves
    tag = "" ## custom tag of the knob to identify it

    click_pos = -1
    num_indicator = 0

    new_value_callback = None ##can be set with a function to be called when the value is updated

    def __init__(self, **kwargs):
        if not kwargs.get('min') == None:
            self.min = kwargs.pop('min')
        if kwargs.get('max'):
            self.max = kwargs.pop('max')
        self.stay_on_mouse_move = True
        ret = super().__init__(**kwargs)
        
        self.root.binder.bind('<ButtonPress-1>', self.knob_mDown) 
        self.root.binder.bind('<ButtonPress-3>', self.knob_rmDown) 
        self.root.binder.bind('<ButtonRelease-1>', self.knob_mUp) 
        self.root.binder.bind('<B1-Motion>', self.knob_mMove) 
        self.root.binder.bind('<MouseWheel>', self.knob_mWheel) 
        self.create_num_indicator(self.num_value)
        self.display_value(self.num_value)
        return ret

    def knob_mWheel(self, event, **kw):
        ## mouse wheel scrolled
        if self.canvas.bbox(self.cimg)[0] < event.x < self.canvas.bbox(self.cimg)[2] and self.canvas.bbox(self.cimg)[1] < event.y < self.canvas.bbox(self.cimg)[3]:
            #click was inside widget
            self.set_num_value(self.num_value + numpy.sign(event.delta))

    def knob_mDown(self, event):
        ## mouse clicked down in window
        if self.canvas.bbox(self.cimg)[0] < event.x < self.canvas.bbox(self.cimg)[2] and self.canvas.bbox(self.cimg)[1] < event.y < self.canvas.bbox(self.cimg)[3]:
            #click was inside widget
            self.display_value(self.num_value)
            self.click_pos=event.y

    def knob_rmDown(self, event, **kw):
        ## mouse right-clicked down in window
        if self.click_pos >= 0:
            self.click_pos = -1
            self.update()

    def knob_mUp(self, event, **kw):
        if self.click_pos >= 0:
            value = (self.click_pos-event.y)*self.speed*(self.max-self.min)/200 + self.num_value
            self.set_num_value(value)
        self.click_pos = -1

    def knob_mMove(self, event, **kw):
        if self.click_pos >= 0:
            self.display_value((self.click_pos-event.y)*self.speed*(self.max-self.min)/200 + self.num_value)

    def display_value(self, value):
        if value < self.min:
            val = self.min
        elif value > self.max:
            val = self.max
        else:
            val = value
        self.rotate_image(self.value_to_degree(val))
        self.update_num_indicator(val)

    def set_num_value(self, value):
        if value < self.min:
            self.num_value = self.min
        elif value > self.max:
            self.num_value = self.max
        else:
            self.num_value = int(value)
        self.display_value(self.num_value)
        if self.new_value_callback:
            self.new_value_callback(self.tag, self.num_value)

    def value_to_degree(self, value):
        span = self.max-self.min
        angle_span = 360-2*self.pad_angle
        angle = value/span*angle_span+self.pad_angle - self.min/span*angle_span
        if angle > (360-self.pad_angle):
            angle = 360-self.pad_angle
        if angle < self.pad_angle:
            angle = self.pad_angle
        return -(angle+self.offset_angle) % 360
    
    def update(self):
        self.set_value(self.num_value)

    def update_num_indicator(self, value):
        self.canvas.delete(self.num_indicator)
        self.create_num_indicator(value)

    def create_num_indicator(self, value):
        self.num_indicator=self.canvas.create_text(self.x, self.y, text=str(int(value)).zfill(4), fill="#333333", font=('Courier 14 bold'))

    def get_rotation_angle(self):
        return self.value_to_degree(self.num_value)