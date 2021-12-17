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
    """abstract class, contains common functionality of SampleListView and PresetListView like displaying files, selecting (soon) moving and renaming them"""
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
    empty = True
    x = 0
    y = 0
    name_width = 240

    
    def __init__(self, master=None, **kw):
        self.root = master
        self.frame = Frame(self.root)
        self.frame.place(x=self.x,y=self.y)
        self.file_list = kw.pop('file_list')
        columns = ('id', 'index', 'name', 'file_name')
        kw.setdefault('columns', columns)

        # style the tree
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("flstyle.Treeview", highlightthickness=0, bd=0, font=('Courier New', 10), background="#cccccc") # Modify the font of the body
        style.configure("flstyle.Treeview.Heading", font=('Courier New', 12,'bold')) # Modify the font of the headings
        #style.layout("flstyle.Treeview", [('flstyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        kw.setdefault('style', "flstyle.Treeview")

        if kw.get('context_entries'):
            self.centries = kw.pop('context_entries')
        self.init_context_menu()
        kw.setdefault('height', 7)
        kw.setdefault('show', 'headings')

        ## Instatiate parent (actual Treeview
        super().__init__(self.frame, **kw)
        
        # define headings
        self.column('id', stretch=NO, minwidth=0, width=0)
        self.column("index",anchor=W, stretch=False, minwidth=25, width=25)
        self.column("name",anchor=W, stretch=0, minwidth=self.name_width, width=self.name_width)
        self.column("file_name",anchor=E, stretch=0, minwidth=70, width=70)
        self.heading('index', text='#', anchor=W)
        self.heading('name', text='Name', anchor=CENTER)
        self.heading('file_name', text='File', anchor=E)
        self.insert('', tk.END, values=('0', '0', '<NO SAMPLES>', '--.--'))
        self.grid(row=0, column=0, sticky=tk.NSEW)
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.yview)
        self.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.update()

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
        inside_widget=event.widget==self
        if inside_widget and not self.identify_region(event.x, event.y) == 'nothing':
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
        if event.widget==self:
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

    def set_files(self, files):
        ## updates the table with a new list of samples, used frequently to assure sync between list in FileList.py and here
        self.delete(*self.get_children())
        if len(files)==0:
            self.insert('', tk.END, values=('0', '0', '<NO FILES>', '--.--'))
            self.empty=True
        else:
            self.empty=False
        for i, sample in enumerate(files):
            self.insert('', tk.END, values=(i, sample.index, sample.name, sample.file_name.upper()))
        self.root.preset_area.redraw()

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
        if file:
            new_name = simpledialog.askstring(title = "Rename File", prompt = "New Name:", initialvalue=file.name, parent = self.root)
            if new_name:
                file.name = new_name
                self.update()

    def key_pressed(self, key):
        if key.keysym=="F2" and self.focus_get()==self:
            ## rename current selection
            if self.selection():
                last_sample = self.file_list.get_file_by_name(self.item(self.selection()[-1])['values'][3])
                self.open_rename_dialog(last_sample)

    def select_file(self, file_name):
        self.selection_set([])
        if file_name:
            for child in self.get_children():
                if self.item(child)['values'][3].lower() == file_name.lower():
                    self.selection_set(child)
                    self.see(child)

    def select_index(self, index):
        self.selection_set([])
        self.selection_set(self.get_children()[index])

    def list_edited(self):
        self.root.preset_area.redraw()
        self.bbox()

    def is_drag_dropped(self, event):
        ##checks if the element is dragged from/to
        return event.widget == self

    def drop_data(self, event, data):
        ## called when a drag&drop cursor drops data to the element
        pass

    def drop_move(self, event, data):
        ## called while a drag&drop cursor is moving over the element
        pass

    def drop_start(self, event, data):
        ## called when a drag&drop action is started for all targets
        pass

    def drop_end(self):
        ## called when drag&drop operation ended or cancelled
        pass