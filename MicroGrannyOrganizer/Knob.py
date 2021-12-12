import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from PIL import *

class Knob(object):
    min = 0    ##min-value for the knob scale
    max = 127  ##max-value for the knob scale
    value = 28 ##current value
    pad_angle = 30 ##angle (from bottom of knob) to where scale starts/ends
    offset_angle = 180 ##offset to orient the knob
    speed = 0.5  ##how fast the knob moves
    label = "Crush" ##name of the knob

    root = 0
    canvas = 0
    img = 0
    img_file = 0
    img_canv = 0
    click_pos = -1
    num_indicator = 0
    label_canv = 0

    def __init__(self, root, canvas, x, y, min, max, name):
        self.label = name
        self.min=min
        self.max=max
        self.canvas = canvas
        self.root = root
        self.img_file = Image.open("images\\knob.png").resize((80, 80), Image.ANTIALIAS)
        self.img=ImageTk.PhotoImage(self.img_file)
        self.img_canv=self.canvas.create_image(x, y, image=self.img)
        self.root.binder.bind('<ButtonPress-1>', self.mDown) 
        self.root.binder.bind('<ButtonPress-3>', self.rmDown) 
        self.root.binder.bind('<ButtonRelease-1>', self.mUp) 
        self.root.binder.bind('<B1-Motion>', self.mMove) 
        self.create_num_indicator(self.value)
        self.display_value(self.value)
        self.create_label()
        return super().__init__()

    def mDown(self, event):
        ## mouse clicked down in window
        if self.canvas.bbox(self.img_canv)[0] < event.x < self.canvas.bbox(self.img_canv)[2] and self.canvas.bbox(self.img_canv)[1] < event.y < self.canvas.bbox(self.img_canv)[3]:
            self.display_value(self.value)
            self.click_pos=event.y

    def rmDown(self, event):
        ## mouse right-clicked down in window
        if self.click_pos >= 0:
            self.click_pos = -1
            self.update()

    def mUp(self, event):
        if self.click_pos >= 0:
            value = (self.click_pos-event.y)*self.speed + self.value
            self.set_value(value)
        self.click_pos = -1

    def mMove(self, event):
        if self.click_pos >= 0:
            self.display_value((self.click_pos-event.y)*self.speed + self.value)

    def display_value(self, value):
        if self.min < value < self.max:
            self.img=ImageTk.PhotoImage(self.img_file.rotate(self.value_to_degree(value)))
            test = self.canvas.create_image(self.canvas.coords(self.img_canv)[0], self.canvas.coords(self.img_canv)[1], image=self.img)
            self.update_num_indicator(value)
            self.canvas.delete(self.img_canv)
            self.img_canv = test

    def set_value(self, value):
        if value < self.min*1.05:
            self.value = self.min
        elif value > self.max * 0.95:
            self.value = self.max
        else:
            self.value = value
        self.display_value(self.value)

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
        self.set_value(self.value)

    def update_num_indicator(self, value):
        self.canvas.delete(self.num_indicator)
        self.create_num_indicator(value)

    def create_num_indicator(self, value):
        self.num_indicator=self.canvas.create_text(self.canvas.coords(self.img_canv)[0], self.canvas.coords(self.img_canv)[1], text=str(int(value)).zfill(4), fill="red", font=('Courier 15 bold'))

    def create_label(self):
        coor= self.canvas.coords(self.img_canv)
        self.label_canv=self.canvas.create_text(coor[0], coor[1], text=self.label, fill="red", font=('Courier 12 bold'), justify=RIGHT)
        knob_width = self.canvas.bbox(self.img_canv)[2] - self.canvas.bbox(self.img_canv)[0]
        self.canvas.move(self.label_canv, -((self.canvas.bbox(self.label_canv)[2]-self.canvas.bbox(self.label_canv)[0])/2+knob_width/2), 0)
    