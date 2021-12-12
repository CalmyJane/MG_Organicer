from FileListView import FileListView

class PresetListView(FileListView):
    """displays all presets on card"""


    def get_list(self):
        return self.file_list.presets