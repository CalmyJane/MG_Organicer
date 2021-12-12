from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk
from tkinter import Text
from tkinter import Toplevel
from tkinter import Button
from tkinter import Label
from tkinter import simpledialog
from tkinter import *

class FileListView(ttk.Treeview):
    """abstract class, contains common functionality of SampleListView and PresetListView"""
    right_mouse_clicked = 0             ## the menu popup window
    frame = 0                           ## stores reference of tkinter root node
    root = 0                            ## stores reference of the frame the tree and scrollbar are in
    file_list = 0                       ## stores the FileList object with all samples inside to edit it on menu selection
    menu_pos = 0
    menu_pos_x = 0
    menu_pos_y = 0
    centries = []                       ## contains array of tuple with context menu entries to add from child
    edit = 0                            ##edit-textinput
    edit_text = 0
    edit_file = 0

    
    def __init__(self, master=None, **kw):
        self.root = master.master
        self.frame = master
        self.file_list = kw.pop('file_list')
        if kw.get('context_entries'):
            self.centries = kw.pop('context_entries')
        self.init_context_menu()
        super().__init__(master=master, **kw)

    def init_context_menu(self):
        self.popup_menu = tk.Menu(self.root, tearoff=0)
        for ce in self.centries:
            self.popup_menu.add_command(label=ce[0], command=ce[1])
        self.popup_menu.add_command(label="Rename", command=self.menu_rename)
        self.popup_menu.add_command(label="Delete", command=self.menu_delete)
        self.popup_menu.add_command(label="Select All", command=self.menu_select_all)

        self.root.binder.bind("<ButtonRelease-3>", self.right_mouse_clicked) # Button-2 on Aqua

        # Register delete button to delete selected samples
        self.root.binder.bind('<Delete>', self.delete_pressed)
        self.root.binder.bind('<Key>', self.key_pressed)

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
                    self.menu_pos_x = event.x
                    self.menu_pos_y = event.y
            finally:
                self.popup_menu.grab_release()
    
    def delete_pressed(self, event):
        self.menu_delete()

    def menu_delete(self):
        ## Menu Selection - delete selected
        for i, csel in enumerate(self.selection()):
            file_name = self.item(csel)['values'][3]
            self.file_list.remove_by_name(file_name)
        self.set_files(self.get_list())

    @abstractmethod
    def get_list(self):
        ##should be overwritten by childs to output either sample-list or preset-list
        return None

    def set_files(self, samples):
        ## updates the table with a new list of samples, used frequently to assure sync between list in FileList.py and here
        self.delete(*self.get_children())
        if len(samples)==0:
            self.insert('', tk.END, values=('0', '0', '<NO FILES>', '--.--'))
        for i, sample in enumerate(samples):
            self.insert('', tk.END, values=(i, sample.index, sample.name, sample.file_name.upper()))

    def menu_select_all(self):
        ## Menu Selection - Select all
        self.selection_set(self.get_children())

    def update(self):
        self.set_files(self.get_list())

    def menu_rename(self):
        ## Menu Selection - rename element   
        self.edit_file = self.file_list.get_file_by_name(self.item(self.get_children()[self.menu_pos])['values'][3])
        self.open_rename_dialog(self.edit_file)

    def open_rename_dialog(self, file):
        new_name = simpledialog.askstring(title = "Rename File", prompt = "New Name:", initialvalue=file.name, parent = self.root)
        if new_name:
            file.name = new_name
            self.update()

    def key_pressed(self, key):
        if key.keysym=="F2":
            ## rename current selection
            if self.selection():
                last_sample = self.file_list.get_file_by_name(self.item(self.selection()[-1])['values'][3])
                self.open_rename_dialog(last_sample)