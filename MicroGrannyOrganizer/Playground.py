import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from PIL import *

def main():

    root = Tk()
    # Add image file
    bg = PhotoImage(file = "images\\Menu_BG.png")
    root.minsize(width=bg.width()+10, height=bg.height()+10)
    root.resizable(False, False)
  
    # Show image using label
    bg_canvas = Canvas(root, width=bg.width()+5, height=bg.height()+5)
    bg_canvas.create_image(bg.width()/2+5, bg.height()/2+5, image=bg)
    knob = Knob(root, bg_canvas, 950, 150, 0, 127)
    bg_canvas.place(x = 0, y = 0)


    load_btn = Button(root, text="Load", fg="black",height= 1, width=10)
    load_btn.place(x=300, y=150)

    write_btn = Button(root, text="Write", fg="red", padx=1,height= 1, width=10)
    write_btn.place(x=150, y=150)



    #root.grid_rowconfigure(0, weight=1)
    #root.grid_columnconfigure(0, weight=1)

    root.mainloop()

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

    def __init__(self, root, canvas, x, y, min, max):
        self.min=min
        self.max=max
        self.canvas = canvas
        self.root = root
        self.img_file = Image.open("images\\knob.png")
        self.img=ImageTk.PhotoImage(self.img_file)
        self.img_canv=self.canvas.create_image(x, y, image=self.img)
        self.root.bind('<ButtonPress-1>', self.mDown) 
        self.root.bind('<ButtonPress-3>', self.rmDown) 
        self.root.bind('<ButtonRelease-1>', self.mUp) 
        self.root.bind('<B1-Motion>', self.mMove) 
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
        angle = value/span*angle_span+self.pad_angle
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
        self.num_indicator=self.canvas.create_text(self.canvas.coords(self.img_canv)[0], self.canvas.coords(self.img_canv)[1], text=str(int(value)).zfill(4), fill="red", font=('Courier 18 bold'))

    def create_label(self):
        coor= self.canvas.coords(self.img_canv)
        self.label_canv=self.canvas.create_text(coor[0], coor[1], text=self.label, fill="red", font=('Courier 22'))
        print(self.canvas.bbox(self.label_canv))
        knob_width = self.canvas.bbox(self.img_canv)[2] - self.canvas.bbox(self.img_canv)[0]
        self.canvas.move(self.label_canv, -((self.canvas.bbox(self.label_canv)[2]-self.canvas.bbox(self.label_canv)[0])/2+knob_width/2), 0)
    
#import wave

#af = wave.open('C:\\Users\\FreshBob\\Downloads\\Sample.wav', 'rb')
#af.setnchannels(1)
#af.setparams((1, 2, 22010, 0, 'NONE', 'Uncompressed'))
#audioData = af.readframes(1)
#print(audioData)
#af.close()

##af = wave.open('C:\\Users\\JGO\\Downloads\\TestSample_Formatted.wav', 'w')
##af.setnchannels(1)
##af.setparams((1, 2, 22010, 0, 'NONE', 'Uncompressed'))
##af.writeframes(audioData)
##af.close()


