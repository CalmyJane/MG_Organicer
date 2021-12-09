import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
from Sample import Sample
from Preset import Preset
from tkinter import filedialog as fd
#from playsound import playsound


class AppWindow(tk.Tk):
    sample_tree = 0
    file_list = 0
    frame = 0

    def __init__(self, file_list):
        super().__init__()
        self.file_list = file_list
        self.frame = Frame(self)
        #self.frame.pack()
        self.geometry('400x400')
        self.title("MicroGranny ORGANICER")
        self.iconbitmap("images/AppIcon.ico")
        self.resizable(False, False)
        self.create_sample_tree()

    def create_sample_tree(self):
        columns = ('id', 'index', 'name', 'file_name')
        self.sample_tree = SampleView(self, columns=columns, show='headings', file_list=self.file_list)
        self.sample_tree.pack()
        # define headings
        self.sample_tree.column('id', stretch=NO, minwidth=0, width=0)
        self.sample_tree.column("index",anchor=W, stretch=False, minwidth=35, width=35)
        self.sample_tree.column("name",anchor=CENTER, stretch=0, minwidth=200, width=200)
        self.sample_tree.column("file_name",anchor=E, stretch=0, minwidth=70, width=70)
        self.sample_tree.heading('index', text='#')
        self.sample_tree.heading('name', text='Name')
        self.sample_tree.heading('file_name', text='File Name')
        self.sample_tree.insert('', tk.END, values=('0', '<NO SAMPLES>', '--.--'))
        self.sample_tree.grid(row=0, column=0, sticky=tk.NSEW)
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.sample_tree.yview)
        self.sample_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

    def set_samples(self, samples):
        self.sample_tree.delete(*self.sample_tree.get_children())
        for i, sample in enumerate(samples):
            self.sample_tree.insert('', tk.END, values=(i, sample.index, sample.name, sample.file_name.upper()))
        
    def delete_samples(self, ifrom, ito):
        self.sample_tree.delete(*self.sample_tree.get_children()[ifrom:ito])


class MainWindow(tk.Frame):
    """represents the main window of the class"""

    def __init__(self, master=None, cnf={}, **kw):
        sample_view = SampleView()
        root.mainloop()
        return super().__init__(master=master, cnf=cnf, **kw)

class SampleView(ttk.Treeview):
    """creates a Tree/Listview of samples using tkinter as UI Library"""
    popup = 0           ## the menu popup window
    root = 0            ## stores reference of tkinter root node
    file_list = 0       ## stores the FileList object with all samples inside to edit it on menu selection
    menu_pos = 0

    def __init__(self, master=None, **kw):
        self.root = master
        self.file_list = kw.pop('file_list')
        self.init_context_menu()
        super().__init__(master=master, **kw)

    def init_context_menu(self):
        self.popup_menu = tk.Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label="Play", command=self.menu_play)
        self.popup_menu.add_command(label="Add", command=self.menu_add_after)
        self.popup_menu.add_command(label="Delete", command=self.menu_delete)
        self.popup_menu.add_command(label="Delete", command=self.menu_delete)
        self.popup_menu.add_command(label="Select All", command=self.menu_select_all)

        self.root.bind("<ButtonRelease-3>", self.popup) # Button-2 on Aqua

    def popup(self, event):
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
        path = self.file_list.get_file_by_name(filename).path
        path.replace("\\", "/")
        print(path)
        #ps = playsound(path)

    def menu_add_after(self):
        ## menu selection - add file via dialog
        filetypes=(("Audio Files", ".wav .ogg"))
        filename = fd.askopenfilename(title='Open a file', initialdir='/')
        if filename:
            sample = Sample(filename, self.file_list.get_free_sample_name())
            sample.index = self.menu_pos + 1
            self.file_list.samples.insert(sample.index, sample)
            self.insert('', self.menu_pos,  values=(1234, sample.index, sample.name, sample.file_name))
            self.set_samples(self.file_list.samples)

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
    frame = MainFrame(app)
    app.mainloop()