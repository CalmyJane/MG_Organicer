import os
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import *
from Sample import Sample
from Preset import Preset
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import tkinter.font as font
import winsound
import wave
import Globals
from FileList import FileList
from Knob import Knob
from Binder import Binder
from PresetArea import PresetArea
from SampleListView import SampleListView
from PresetListView import PresetListView
from ButtonBar import ButtonBar

class AppWindow(tk.Tk):
    sample_tree = 0             ## tkinter TreeView with scrollbar and context menu
    file_list = 0               ## contains data of all presets/samples and the nametable
    tree_frame = 0              ## frame that holds the sample-tree
    bg = 0                      ## PhotoImage-object of the background image
    bg_label = 0                ## label-object that stores the background image 'bg'
    load_btn = 0                ## reference of the load-button object
    write_btn = 0               ## reference of the write-button object
    auto_play = 0               ## reference to the autoplay-checkbox
    autoplay_value = 1          ## wether the autoplay checkbox is set or not (1, 0)
    canvas = 0                  ## canvas holds background image and knobs
    binder = 0                  ## tool to allow multiple callbacks to an event like <ButtonPress-1>
    preset_area = 0             ## PresetView-Object holding all UI elements related to a preset
    preset_tree = 0             ## PresetList
    button_bar = 0              ## holding the 6 sample buttons

    def __init__(self):
        super().__init__()
        # Init binder
        self.binder = Binder(self)
        # Read files from card
        self.load_file_list(Globals.SD_CARD_PATH)

        ##Init UI Window
        self.title("MicroGranny ORGANICER")
        self.iconbitmap("images/AppIcon.ico")
        self.iconbitmap(default="images/AppIcon.ico")
        self.resizable(False, False)

        # create canvas for background and PresetView
        self.bg = PhotoImage(file = "images\\Menu_BG.png")
        self.minsize(width=self.bg.width()+10, height=self.bg.height()+10)
        self.canvas = Canvas(self, width=self.bg.width()+5, height=self.bg.height()+5)
        self.canvas.create_image(self.bg.width()/2+5, self.bg.height()/2+5, image=self.bg)
        self.canvas.place(x = 0, y = 0)

        # create Preset Area, knobs, setting-indicators ...
        self.preset_area = PresetArea(self, self.canvas, self.file_list)

        # Create Buttons
        self.create_buttons()

        # Create Sample Tree
        self.sample_tree = SampleListView(self, file_list=self.file_list)

        # Create Preset Tree
        self.preset_tree = PresetListView(self, preset_area=self.preset_area, file_list=self.file_list)

        print(self.file_list.get_file_by_name('P01.txt').slots[2][8])

    def create_buttons(self):
        button_font = font.Font(family='Courier New', size=20, weight='bold')
        # Create Buttons
        load_btn = Button(self, text="Load", fg="black",height= 2, width=9, command=self.load_pressed, bd=3, font=button_font)
        load_btn.place(x=70, y=450)

        write_btn = Button(self, text="Write", fg="red", height= 2, width=9, command=self.write_pressed, bd=3, font=button_font)
        write_btn.place(x=240, y=450)

        # Create Checkbox for autoplay
        self.autoplay_value = tk.BooleanVar()
        self.auto_play = tk.Checkbutton(self, text="auto-play", variable=self.autoplay_value, onvalue=True, offvalue=False, command=self.auto_play_toggled)
        self.autoplay_value.set(True)
        self.auto_play.place(x=70, y=420)

    def auto_play_toggled(self):
        self.sample_tree.auto_play = self.autoplay_value.get()
        self.sample_tree.stop_playing()

    def load_pressed(self):
        ## load new folder from dialog
        target_folder = fd.askdirectory(title="Select Folder or SD-Card")
        if target_folder:
            if len(target_folder) <= 4:
                # folder is a Drive, e.g. 'G:\\'
                mb.showwarning('SD Card Selected', 'It is recommended to work in a folder on your drive to avoid extensive usage of the SD-Card.')
            self.load_file_list(target_folder + "\\")

    def load_file_list(self, path):
        Globals.SD_CARD_PATH = path
        self.file_list = FileList()
        if self.sample_tree:
            self.sample_tree.file_list = self.file_list
            self.sample_tree.update()
        if self.preset_tree:
            self.preset_tree.file_list = self.file_list
            self.preset_tree.update()

    def write_pressed(self):
        write_msg = 'It is recommended to create of your SD-Card before writing from this tool. \n'
        write_msg += str(len(self.file_list.removed_files)) + ' files will be deleted. \n'
        write_msg += str(self.file_list.get_num_new_files()) + ' files will be added. \n'
        if mb.askokcancel('Modiying Files', write_msg):
            self.file_list.write_to_card()
            mb.showinfo("Updated Successfull", "Your files have been updated.")
            self.load_file_list(Globals.SD_CARD_PATH)

if __name__ == "__main__":
    app = App()
    tree_frame = MainFrame(app)
    app.mainloop()