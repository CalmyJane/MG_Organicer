import winsound
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import Frame
from Sample import Sample
from FileListView import FileListView

class SampleListView(FileListView):
    """The Table of all samples"""
    auto_play = True        ## play samples when clicked in tree?

    def __init__(self, master=None, **kw):
        kw.setdefault("context_entries", (("Play", self.play),("Add After", self.add_after)))
        master.binder.bind("<<TreeviewSelect>>", self.selection_change) # Button-2 on Aqua
        kw.setdefault('height', 16)
        self.position_x = 70
        self.position_y = 71
        self.name_width = 200

        return super().__init__(master=master, **kw)

    def play(self):
        ## menu selection - play selected file
        filename = self.item(self.get_children()[self.menu_pos])['values'][3]
        if not filename=="--.--":
            self.file_list.get_file_by_name(filename).play()

    def stop_playing(self):
        winsound.PlaySound(None, winsound.SND_PURGE)

    def selection_change(self, event):
        ## user changed selection via mouse or arrow-keys
        if event.widget==self:
            if self.selection():
                currSample = self.file_list.get_file_by_name(self.item(self.selection()[-1])['values'][3])
            if self.auto_play and len(self.selection()) > 0 and currSample:
                currSample.play()

    def add_after(self):
        ## menu selection - add file via dialog
        filetypes=(("Audio .wav", "Audio .wav"))
        filenames = fd.askopenfilenames(title='Select Sample(s)', filetypes=filetypes)
        if filenames:
            for i, filename in enumerate(filenames):
                sample = Sample(filenames[len(filenames)-i-1], self.file_list.get_free_sample_name())
                sample.index = self.menu_pos + 1
                self.file_list.insert_sample(sample.index, sample)
                self.insert('', self.menu_pos,  values=(1234, sample.index, sample.name, sample.file_name))
            self.set_files(self.get_list())

    def get_list(self):
        ##overwrites parent method to tell which list to use
        return self.file_list.samples
