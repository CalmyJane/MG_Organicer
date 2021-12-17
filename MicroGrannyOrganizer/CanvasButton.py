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
    drop_img='images\\button_drop.png' ## image in accept-drop-state
    ion_img=0 ## image object in on-state
    ioff_img=0 ## image object in off-state
    idis_img=0 ## image object in disabled-state
    ihigh_img=0 ## image object in highlight-state
    idrop_img=0 ## image object in drop-state
    tkon_img=0 ## TKImage Object on-state
    tkoff_img=0 ## TKImage Object in off-state
    tkdis_img=0 ## TKImage Object in disabled-state
    tkhigh_img=0 ## TKImage Object in highlight-state
    tkdrop_img=0 ## TKImage Object in drop-state
    cimg=0 ## currently displayed image
    chigh=0 ## highlight-image, overlays cimg
    switch_mode = SwitchModes.switch_until_released
    width = 100 ## width of the image
    height = 100 ## height of the image
    stay_on_mouse_move = False ## set to true to keep the button on in Switch_Until_Released, even if the mouse leaves the button

    label_font = ('Courier 12 bold') ## font of the label
    clabel = 0 ## contains the canvas text-object for label
    label_visible = True ## is the label drawn
    label_offs_x = 0
    label_offs_y = 0
    label_dock = '' ## can contain n, s, e or w for where to dock the labe. Use offset if empty

    value=False ## current value of the button
    value_change_callback = 0 ## function to be called on valuechange, must accept
    clicked_callback = 0 ## function to be called on mousedown on the button
    data_dropped_callback = 0 ## callback when data is dropped on the button from DragnDropper
    canvas:Canvas = 0 ## canvas to draw the button on (required)
    root:tk = 0 ## the root app-object

    clicked = False ## stores if button was clicked to use switch when released on mouseup
    outside = False ## info if cursor was dragged out of button after click
    disabled = False ## is the button clickable or not
    highlighted = False ## is the button highlight-image visible
    dragged_to = False ## true while a file is dragged towards the button
    dragged_on = False ## true while a file is dragged and hovering over the button

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
        if kwargs.get('drop_img'):
            self.drop_img = kwargs.pop('drop_img')
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
        if kwargs.get('stay_on_mouse_move'):
            self.stay_on_mouse_move = kwargs.pop('stay_on_mouse_move')
        if not kwargs.get('label_dock') == None:
            self.label_dock = kwargs.pop('label_dock')
        self.value_change_callback = self.default_callback
        self.clicked_callback = self.default_callback
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
        self.idrop_img = Image.open(self.drop_img).resize((self.width, self.height), Image.ANTIALIAS)
        self.tkon_img=ImageTk.PhotoImage(self.ion_img)
        self.tkoff_img=ImageTk.PhotoImage(self.ioff_img)
        self.tkdis_img=ImageTk.PhotoImage(self.idis_img)
        self.tkhigh_img=ImageTk.PhotoImage(self.ihigh_img)
        self.tkdrop_img=ImageTk.PhotoImage(self.idrop_img)
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
        if self.clicked and not self.stay_on_mouse_move:
            if self.switch_mode == SwitchModes.switch_until_released:
                # if switch until released, track if curser moves out and back in again, and toggle button accordingly
                # this behavior can be disabled by self.stay_on_mouse_move=True
                bbox = self.canvas.bbox(self.cimg)
                if not inside:
                    if not self.outside:
                        # just moved outside button button area
                        self.outside = True
                        self.switch_off()

                else:
                    # moved inside box
                    if self.outside:
                        #moved back inside
                        self.switch_on()
                        self.outside = False

    def show_highlight(self, show):
        self.highlighted = show
        self.tkhigh_img=ImageTk.PhotoImage(self.ihigh_img.rotate(self.get_rotation_angle()))
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
        if self.disabled:
            img = self.cimg
            self.cimg = self.canvas.create_image(self.x, self.y, image=self.tkdis_img)
            self.canvas.delete(img)
        else:
            set_value(self.value)

    def redraw(self):
        self.rotate_image(self.get_rotation_angle())
        if self.label_visible:
            self.draw_label()

    def draw_label(self):
        self.canvas.delete(self.clabel)
        if self.label_dock == 'left':
            self.clabel=self.canvas.create_text(self.x, self.y+self.label_offs_y, text=self.label, fill="silver", font=self.label_font, justify=RIGHT)
            xpos = -((self.canvas.bbox(self.clabel)[2]-self.canvas.bbox(self.clabel)[0])/2+self.width/2+5) ##calculate offset to the left
            self.canvas.move(self.clabel, xpos, 0) ## move by offset
        elif self.label_dock == 'right':
            self.clabel=self.canvas.create_text(self.x, self.y+self.label_offs_y, text=self.label, fill="silver", font=self.label_font, justify=RIGHT)
            xpos = (self.canvas.bbox(self.clabel)[2]-self.canvas.bbox(self.clabel)[0])/2+self.width/2+5 ##calculate offset to the right
            self.canvas.move(self.clabel, xpos, 0) ## move by offset
        elif self.label_dock == 'down':
            self.clabel=self.canvas.create_text(self.x, self.y+self.label_offs_y, text=self.label, fill="silver", font=self.label_font, justify=RIGHT)
            ypos = (self.canvas.bbox(self.clabel)[3]-self.canvas.bbox(self.clabel)[1])/2+self.height/2-5 ##calculate offset down
            self.canvas.move(self.clabel, 0, ypos) ## move by offset
        elif self.label_dock == 'up':
            self.clabel=self.canvas.create_text(self.x, self.y+self.label_offs_y, text=self.label, fill="silver", font=self.label_font, justify=RIGHT)
            ypos = -((self.canvas.bbox(self.clabel)[3]-self.canvas.bbox(self.clabel)[1])/2+self.height/2) ##calculate offset up
            self.canvas.move(self.clabel, 0, ypos) ## move by offset
        else:
            self.clabel=self.canvas.create_text(self.x+self.label_offs_x, self.y+self.label_offs_y, text=self.label, fill="silver", font=self.label_font, justify=CENTER)

    def rotate_image(self, angle):
        self.canvas.delete(self.cimg)
        #rotate images
        self.tkdis_img=ImageTk.PhotoImage(self.idis_img.rotate(angle))
        self.tkon_img=ImageTk.PhotoImage(self.ion_img.rotate(angle))
        self.tkoff_img=ImageTk.PhotoImage(self.ioff_img.rotate(angle))
        self.tkdrop_img=ImageTk.PhotoImage(self.idrop_img.rotate(angle))
        if self.disabled:
            tkimg = self.tkdis_img
        elif self.dragged_on:
            tkimg = self.tkdrop_img##turn drop-accept when file is dragged above button
        elif self.dragged_to:
            tkimg=self.tkon_img##tur on when file is dragged towards button
        elif self.value:
            tkimg = self.tkon_img
        else:
            tkimg = self.tkoff_img
        #draw image
        self.cimg = self.canvas.create_image(self.x, self.y, image=tkimg)
        if self.highlighted:
            self.tkhigh_img=ImageTk.PhotoImage(self.ihigh_img.rotate(angle))
            self.chigh = self.canvas.create_image(self.x, self.y, image=self.tkhigh_img)

    def get_rotation_angle(self):
        ##overwritten by children, returns the current angle if needed
        return 0

    def is_drag_dropped(self, event):
        bbox = self.canvas.bbox(self.cimg)
        bbox = (self.x-self.width, self.y-self.height, self.x, self.y)
        isdrag = bbox[0]<event.x<bbox[2] and bbox[1]<event.y<bbox[3]
        return isdrag

    def drop_data(self, event, data):
        ## called when a drag&drop cursor drops data to the element
        if self.data_dropped_callback:
            self.data_dropped_callback(self, data) ## forward drop information to caller

    def drop_move(self, event, data):
        ## called while a drag&drop cursor is moving over the element
        ## if drop-cursor is over button set dragged_on true
        self.dragged_on=self.is_drag_dropped(event)
        self.redraw()

    def drop_start(self, event, data):
        ## called when a drag&drop action is started for all targets
        self.dragged_to = True
        self.redraw()

    def drop_end(self):
        self.dragged_on = False
        self.dragged_to = False
        self.redraw()