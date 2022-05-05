from tkinter import *
import Left_Area
class Transmit_Container:
    def __init__(self, parent, **kw):
        self.parent = parent
        self.wrapper = Frame(self.parent)
        self.wrapper.place(rely=0, relx=0, relheight=1, relwidth=.48)
        self.area = Frame(self.wrapper, borderwidth=1)
        self.area.place(rely=.01, relx=.01, relheight=.97, relwidth=.98)
        self.sections = []
        self.sections.append(Frame(self.area, bg="green", relief=RAISED, borderwidth=1).pack(fill=BOTH, expand=True, side=BOTTOM))


basic_settings.place(rely=0, relx=0, height=150, relwidth=1)

freq_container = Frame(basic_settings, bg="#afb0b3")
freq_container.place(rely=0.01, relx=.01, height=70, relwidth=.52)

bw_container = Frame(basic_settings, bg="#afb0b3")
bw_container.place(y=75, relx=.01, height=70, relwidth=.52)

intermediate_settings = Frame(left_container, bg="#afb0b3", relief=RAISED, borderwidth=1)
intermediate_settings.place(y=155, relx=0, relheight=1, relwidth=1)

sample_container = Frame(intermediate_settings, bg="#afb0b3")
sample_container.place(y=5, relx=.01, height=70, relwidth=.96)

ch_ctrl_container = Frame(intermediate_settings, bg="#afb0b3")
ch_ctrl_container.place(y=75, relx=.01, height=70, relwidth=.96)

# gain_container = Frame(left_container, bg="#afb0b3")
# gain_container.place(rely=0.635, relx=.01, height=70, relwidth=.96)

tx_ctrl_container = Frame(intermediate_settings, bg="#afb0b3")
tx_ctrl_container.place(y=145, relx=.01, height=70, relwidth=.96)

pwr_root = Frame(intermediate_settings, bg="#afb0b3")
pwr_root.place(y=220, relx=.03, height=200, relwidth=.95)
pwr_tab = ttk.Notebook(pwr_root)

pwr_container = Frame(pwr_tab, bg="#afb0b3")
pwr_adv_tab = Frame(pwr_tab, bg="#afb0b3")
pwr_tab.add(pwr_container, text="Basic")
pwr_tab.add(pwr_adv_tab, text="Advanced")
pwr_tab.pack(expand=1, fill='both')