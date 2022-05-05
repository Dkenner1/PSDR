from tkinter import *

class LabeledText:

    def __init__(self, parent, text, callback):
        self.parent = parent
        self.wrapper = Frame(self.parent)
        self.wrapper.place(rely=0, relx=0, relheight=1, relwidth=.48)
        self.area = Frame(self.wrapper, borderwidth=1)
        self.area.place(rely=.01, relx=.01, relheight=.97, relwidth=.98)


freq_label = Button(freq_container, text="Frequency",
                    fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o, "freq"))
freq_label.place(rely=0.05, relx=0.05, height=70, width=145)

freq_widg = Entry(freq_container, bg="white", relief=SUNKEN, font=ctrl_font)
freq_widg.place(rely=0.14, x=173, height=50, width=140)
freq_widg.insert(END, p.int2SI(int(config['freq'])) + "Hz")
freq_widg.focus_set()