import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
from Sample import Sample
from Preset import Preset
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import winsound
import wave
import Globals
from FileList import FileList

class AppWindow(tk.Tk):
    sample_tree = 0             ## tkinter TreeView with scrollbar and context menu
    file_list = 0               ## contains data of all presets/samples and the nametable
    tree_frame = 0              ## frame that holds the sample-tree
    bg = 0                      ## PhotoImage-object of the background image
    bg_label = 0                ## label-object that stores the background image 'bg'
    load_btn = 0                ## reference of the load-button object
    write_btn = 0               ## reference of the write-button object

    def __init__(self):
        super().__init__()

        # Read files from card
        self.load_file_list(Globals.SD_CARD_PATH)

        ##Init UI Window
        self.title("MicroGranny ORGANICER")
        self.iconbitmap("images/AppIcon.ico")

        # Add image file
        self.bg = PhotoImage(file = "images\\Menu_BG.png")
        self.minsize(width=self.bg.width()+5, height=self.bg.height()+5)
        self.resizable(False, False)
  
        # Show background image using label
        self.bg_label = Label(self, image = self.bg)
        self.bg_label.place(x = 0, y = 0)

        # Create Buttons
        self.create_buttons()

        # Create Sample Tree
        self.tree_frame = Frame(self)
        self.tree_frame.place(x=70, y=71)
        self.create_sample_tree()
        self.sample_tree.set_samples(self.file_list.samples)

    def create_buttons(self):
        # Create Buttons
        load_btn = Button(self, text="Load", fg="black",height= 5, width=20, command=self.load_pressed)
        load_btn.place(x=70, y=450)

        write_btn = Button(self, text="Write", fg="red", padx=1,height= 5, width=20, command=self.write_pressed)
        write_btn.place(x=250, y=450)


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
            self.sample_tree.set_samples(self.file_list.samples)

    def write_pressed(self):
        write_msg = 'It is recommended to create of your SD-Card before writing from this tool. \n'
        write_msg += str(len(self.file_list.removed_samples)) + ' files will be deleted. \n'
        write_msg += str(self.file_list.get_num_new_samples()) + ' files will be added. \n'
        if mb.askokcancel('Modiying Files', write_msg):
            self.file_list.write_to_card()
            mb.showinfo("Updated Successfull", "Your files have been updated.")
            self.load_file_list(Globals.SD_CARD_PATH)

    def create_sample_tree(self):
        columns = ('id', 'index', 'name', 'file_name')
        self.sample_tree = SampleView(self.tree_frame, height=16, columns=columns, show='headings', file_list=self.file_list)
        self.sample_tree.pack()
        # define headings
        self.sample_tree.column('id', stretch=NO, minwidth=0, width=0)
        self.sample_tree.column("index",anchor=W, stretch=False, minwidth=35, width=35)
        self.sample_tree.column("name",anchor=CENTER, stretch=0, minwidth=200, width=200)
        self.sample_tree.column("file_name",anchor=E, stretch=0, minwidth=70, width=70)
        self.sample_tree.heading('index', text='#')
        self.sample_tree.heading('name', text='Name')
        self.sample_tree.heading('file_name', text='File Name')
        self.sample_tree.insert('', tk.END, values=('0', '0', '<NO SAMPLES>', '--.--'))
        self.sample_tree.grid(row=0, column=0, sticky=tk.NSEW)
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.sample_tree.yview)
        self.sample_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        
    def delete_samples(self, ifrom, ito):
        self.sample_tree.delete(*self.sample_tree.get_children()[ifrom:ito])

class SampleView(ttk.Treeview):
    """creates a Tree/Listview of samples using tkinter as UI Library"""
    right_mouse_clicked = 0           ## the menu popup window
    frame = 0            ## stores reference of tkinter root node
    root = 0           ## stores reference of the frame the tree and scrollbar are in
    file_list = 0       ## stores the FileList object with all samples inside to edit it on menu selection
    menu_pos = 0

    def __init__(self, master=None, **kw):
        self.root = master.master
        self.frame = master
        self.file_list = kw.pop('file_list')
        self.init_context_menu()
        super().__init__(master=master, **kw)

    def init_context_menu(self):
        self.popup_menu = tk.Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label="Play", command=self.menu_play)
        self.popup_menu.add_command(label="Add", command=self.menu_add_after)
        self.popup_menu.add_command(label="Delete", command=self.menu_delete)
        self.popup_menu.add_command(label="Select All", command=self.menu_select_all)

        self.root.bind("<ButtonRelease-3>", self.right_mouse_clicked) # Button-2 on Aqua

        # Register delete button to delete selected samples
        self.root.bind('<Delete>', self.delete_pressed)

    def right_mouse_clicked(self, event):
        ## opens the menu-popup, called when rightclick is activated on main window
        if not self.identify_region(event.x, event.y) == 'nothing':
            #click inside region?
            try:
                row = self.identify_row(event.y)
                if row and len(self.item(row)['values']) > 0:
                    #row was clicked, not header or scrollbar
                    if len(self.selection()) <= 1:
                        self.selection_set([])
                        self.selection_add(row)
                    self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
                    self.menu_pos = self.item(self.identify_row(event.y))['values'][0]
            finally:
                self.popup_menu.grab_release()

    def menu_play(self):
        ## menu selection - play selected file
        filename = self.item(self.get_children()[self.menu_pos])['values'][3]
        self.file_list.get_file_by_name(filename).play()

    def menu_add_after(self):
        ## menu selection - add file via dialog
        filetypes=(("Audio .wav", "Audio .wav"))
        filenames = fd.askopenfilenames(title='Select Sample(s)', filetypes=filetypes)
        if filenames:
            for i, filename in enumerate(filenames):
                sample = Sample(filenames[len(filenames)-i-1], self.file_list.get_free_sample_name())
                sample.index = self.menu_pos + 1
                self.file_list.insert_sample(sample.index, sample)
                self.insert('', self.menu_pos,  values=(1234, sample.index, sample.name, sample.file_name))
                self.set_samples(self.file_list.samples)
    
    def delete_pressed(self, event):
        self.menu_delete()

    def menu_delete(self):
        ## Menu Selection - delete selected
        for i, csel in enumerate(self.selection()):
            file_name = self.item(csel)['values'][3]
            self.file_list.remove_by_name(file_name)
        self.set_samples(self.file_list.samples)

    def set_samples(self, samples):
        ## updates the table with a new list of samples, used frequently to assure sync between list in FileList.py and here
        self.delete(*self.get_children())
        for i, sample in enumerate(samples):
            self.insert('', tk.END, values=(i, sample.index, sample.name, sample.file_name.upper()))

    def menu_select_all(self):
        ## Menu Selection - Select all
        self.selection_set(self.get_children())

if __name__ == "__main__":
    app = App()
    tree_frame = MainFrame(app)
    app.mainloop()