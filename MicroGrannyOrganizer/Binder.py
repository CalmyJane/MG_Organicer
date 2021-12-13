class Binder(object):
    """Helper-Class that allows to register multiple callbacks to a tkinter-event like '<ButtonPress-1>'"""
    events=[]
    root = 0

    def __init__(self, root):
        self.root = root
        return super().__init__()

    def bind(self, identifier, callback):
        index = self.get_event_index(identifier)
        if index >= 0:
            self.events[index].add_callback(callback)
        else:
            ev = Event(self.root, identifier)
            ev.add_callback(callback)
            self.events.append(ev)

    def get_event_index(self, identifier):
        for i, ev in enumerate(self.events):
            if ev.identifier == identifier:
                return i
        return -1

class Event(object):
    ## represents a single event like <ButtonPress-1> and holds multiple callbacks to call when event is triggered
    identifier=""       ## Event Type, e.g. <ButtonPress-1>
    root=0              ## tkinter-root-object
    callbacks = []      ## callback functions for the event

    def __init__(self, root, identifier):
        self.callbacks = []
        self.identifier = identifier
        self.root = root
        return super().__init__()

    def add_callback(self, callback):
        self.callbacks.append(callback)
        self.root.bind(self.identifier, self.event_cb)

    def event_cb(self, event):
        #main callback that calls all linked callbacks
        for cb in self.callbacks:
            cb(event)
