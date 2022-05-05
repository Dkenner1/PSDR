from tkinter import Frame

class Left_Area:
    def __init__(self, parent, **kw):
        self.parent = parent
        self.wrapper = Frame(self.parent)
        self.wrapper.place(rely=0, relx=0, relheight=1, relwidth=.48)
        self.area = Frame(self.wrapper, borderwidth=1)
        self.area.place(rely=.01, relx=.01, relheight=.97, relwidth=.98)

