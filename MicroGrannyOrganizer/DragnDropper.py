
class DragnDropper(object):
    """tracks the mouse and enables user to drag and drop from a source to a target"""

    sources = [] ## a list of objects that can be dragged from, must contain method 'bbox(self)' returning array of x1,y1,x2,y2 and 'get_drag(self)' returning the drag_data
    targets = [] ## list of objects that can be dragged to. must contain 'bbox(self)' and 'set_drag(self, data)' recieving the drag_data

    drag_data=0 ## can contain anything, but source and targets "get_drag" and "set_drag" functions must 'send' and 'recieve' the same thing
    dragging = False ## currently dragging?
    clicked = False ## if a source was clicked, will start draggin on next mouse-move event
    drag_start_event_data = False ## stores the event-data from mousedown event to be used to start drag on mousemove

    def __init__(self, root):
        self.root = root
        self.root.binder.bind('<ButtonPress-1>', self.mDown)
        self.root.binder.bind('<ButtonRelease-1>', self.mUp)
        self.root.binder.bind('<B1-Motion>', self.mMove)
        return super().__init__()

    def add_source(self, source):
        self.sources.append(source)

    def add_target(self, target):
        self.targets.append(target)

    def mDown(self, event):
        ## mouse down - start drag if source was clicked, store drag data and wait for mouse up
        if self.get_source(event):
            self.clicked = True
            self.drag_start_event_data = event
        else:
            self.dragging = False
            self.drag_data = 0

    def mUp(self, event):
        ## mouse released, drop data to target if one was hit
        if self.get_target(event) and self.dragging:
            self.get_target(event).drop_data(event, self.drag_data)
        for el in self.targets+self.sources:
            if el.drop_end:
                el.drop_end()
        self.dragging = False
        self.clicked = False
        self.root.config(cursor='arrow')

    def mMove(self, event):
        if self.clicked:
            self.start_drag(self.drag_start_event_data)
        self.clicked=False
        if self.dragging:
            for target in self.targets:
                target.drop_move(event, self.drag_data)

    def get_source(self, event):
        for source in self.sources:
            if source.is_drag_dropped(event):
                return source

    def get_target(self, event):
        for target in self.targets:
            if target.is_drag_dropped(event):
                return target

    def start_drag(self, event):
        self.drag_data = self.get_source(event).get_drag(event)
        if self.drag_data:
            self.dragging=True
            self.root.config(cursor='fleur')
            for target in self.targets:
                target.drop_start(event, self.drag_data)

