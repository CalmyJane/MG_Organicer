import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk

class MgButton(object):
    """UI Element consisting of a square button, a label and a led that indicates a setting"""
    led = 0 ##led indicator
    canvas = 0 ##canvas to place objects on
    btn = 0 ##button
    lbl = 0 ##label
    blbl = 0 ##button label
    root = 0 ##tkinter root window
    x = 0 ##x-position of the whole element
    y = 0 ##y-position of the whole element


    def __init__(self, **kw):
        self.canvas=kw.pop('canvas')
        self.root=kw.pop('root')
        self.x=kw.pop('x')
        self.y=kw.pop('y')
        self.init_button()
        self.init_led()
        self.init_label()
        self.init_button_label()
        return super().__init__()

    def init_button(self):
        print('init button')
        self.btn = Button(self.root, text="AB", width=5, height=5, command=self.button_pressed)
        self.btn.place(x=self.x, y=self.y)

    def init_led(self):
        print('init_led button')

    def init_label(self):
        print('init_label button')

    def init_button_label(self):
        print('init_button_label button')

    def button_pressed(self):
        print('button pressed')
