#!/usr/bin/env python3
import tkinter.filedialog
from tkinter import *
from tkinter import ttk
import tkinter.font as font
import libs.pylibSDR.pylibSDR.bladeRF as bladeRF
import libs.pylibSDR.constants.bladeRF_const as bladeRF_const
import libs.UnitReader.UnitParser as Parser
import src.py_src.Left_Area as Left_Design
import re
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
import numpy as np
from src.py_src.Elements import Table

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, "etc/bladeRF_TxConfig.ini")
exe_path = os.path.join(dir_path, "bin/RF_enable")

SDR = bladeRF.SDR(exe_path, config_path)
root_win = Tk()
root_win.geometry('1200x640')
root_win.title("BladeRF Control")
root_win.configure(bg="#262A33")
# root_win.attributes('-fullscreen', True)

config = SDR.get_config()
if config['tx'] == '1':
    SDR.disable()
photo = PhotoImage(file=os.path.join(dir_path, "etc/Title.png"))
root_win.iconphoto(False, photo)
p = Parser.UnitParser()


def running():
    return True if int(SDR.get_config()['tx']) else False


def rx_running():
    return True if int(SDR.get_config()['rx']) else False


def help_btn(txt_widg, key):
    if key not in bladeRF_const.HELP_TXT:
        return
    txt_widg.config(state="normal")
    txt_widg.delete("1.0", "end")
    txt_widg.insert(INSERT, re.sub(r"[\t]*", "", bladeRF_const.HELP_TXT[key]))
    txt_widg.config(state="disabled")


def start_ctrl(btn_widg, txt_widg):
    global config
    if not running():
        SDR.enable()
        config = SDR.get_config()
        dump_config(txt_widg)
        btn_widg['text'] = "Stop"
    else:
        SDR.disable()
        txt_widg.config(state="normal")
        txt_widg.delete("1.0", "end")
        txt_widg.insert(INSERT, "Device now stopped\n")
        txt_widg.config(state="disabled")
        btn_widg['text'] = "Transmit"


def rx_ctrl(btn_widg, txt_widg):
    global config
    if rx_running():
        SDR.rx_disable()
        txt_widg.config(state="normal")
        txt_widg.delete("1.0", "end")
        txt_widg.insert(INSERT, "Device now stopped\n")
        txt_widg.config(state="disabled")
        btn_widg['text'] = "Receive"
    else:
        SDR.rx_enable()
        config = SDR.get_config()
        dump_rxconfig(txt_widg)
        btn_widg['text'] = "Stop"


def dump_config(txt_widg):
    txt_widg.config(state="normal")
    txt_widg.delete("1.0", "end")
    txt_widg.insert(INSERT, "Device now running\n\n")
    txt_widg.insert(INSERT, "Configuration State (Note: values displayed are what is in" +
                    "\nthe configuration file)\n\n")
    txt_widg.insert(INSERT, "Frequency" + ": " + p.int2SI(int(config['freq'])) + "Hz\n")
    txt_widg.insert(INSERT, "Bandwidth" + ": " + p.int2SI(int(config['bandwidth'])) + "Hz\n")
    txt_widg.insert(INSERT, "Number Samples" + ": " + p.int2SI(int(config['num_samples'])) + "S\n")
    txt_widg.insert(INSERT, "Sample Rate" + ": " + p.int2SI(int(config['sample_rate'])) + "Sps\n")
    txt_widg.insert(INSERT, "Power" + ": " + config['pwr'] + "dBm\n")
    txt_widg.insert(INSERT, "Tx Mode" + ": " + config['tx_mode'] + "\n")
    txt_widg.insert(INSERT, "Channel Mode" + ": " + config['channel_mode'] + "\n")
    txt_widg.insert(INSERT, "Channel" + ": " + config['channel'] + "\n")
    txt_widg.insert(INSERT, "Duty Cycle" + ": " + config['duty_cycle'] + "\n")
    txt_widg.insert(INSERT, "Enabled" + ": " + config['tx'] + "\n")
    # for key, value in config.items():
    #    txt_widg.insert(INSERT, key + ": " + str(value) + "\n")
    txt_widg.config(state="disabled")


def dump_rxconfig(txt_widg):
    txt_widg.config(state="normal")
    txt_widg.delete("1.0", "end")
    txt_widg.insert(INSERT, "Device now running\n\n")
    txt_widg.insert(INSERT, "Configuration State (Note: values displayed are what is in" +
                    "\nthe configuration file)\n\n")
    txt_widg.insert(INSERT, "Frequency" + ": " + p.int2SI(int(config['rx_freq'])) + "Hz\n")
    txt_widg.insert(INSERT, "Bandwidth" + ": " + p.int2SI(int(config['rx_bandwidth'])) + "Hz\n")
    txt_widg.insert(INSERT, "Number Samples" + ": " + p.int2SI(int(config['rx_num_samples'])) + "S\n")
    rx_sr = p.int2SI(int(config['rx_sample_rate'])) if int(config['auto']) == 0 else p.int2SI(
        int(config['rx_bandwidth']) * 2.4)
    txt_widg.insert(INSERT, "Sample Rate" + ": " + rx_sr + "Sps\n")
    txt_widg.insert(INSERT, "Enabled" + ": " + config['rx'] + "\n")
    # for key, value in config.items():
    #    txt_widg.insert(INSERT, key + ": " + str(value) + "\n")
    txt_widg.config(state="disabled")


def write_text_win(string, txt_widg):
    txt_widg.config(state="normal")
    txt_widg.delete("1.0", "end")
    txt_widg.insert(INSERT, string)
    txt_widg.config(state="disabled")


def update(key, val, txt_widg):
    global config
    if key is None or val is None or txt_widg is None:
        print("No key/val/txt_widg assigned")
        return
    try:
        SDR.update_list[key](val)
        config = SDR.get_config()
        if running():
            dump_config(txt_widg)
        elif rx_running():
            dump_rxconfig(txt_widg)
        else:
            write_text_win("Value Updated Successfully for Key: " + key, txt_widg)

    except ValueError as err:
        write_text_win(str(err), txt_widg)


def entry_submit(e, key, txt_widg=None):
    widget = e.widget
    if type(widget) is not type(Entry()) or type(txt_widg) is not type(Text()):
        return
    update(key, Parser.SI2int(widget.get()), txt_widg)


def get_all_entry_widgets_text_content(parent_widget):
    children_widgets = parent_widget.winfo_children()
    for child_widget in children_widgets:
        if child_widget.winfo_class() == 'Entry':
            print(child_widget.get())


def multi_func(*funcs):
    def func_list(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return func_list


def lock_duty_cycle(duty_entry, mode):
    duty_entry['state'] = 'normal'
    duty_entry.delete("0", END)
    if mode == bladeRF_const.TxMode_CONTINUOUS:
        duty_entry.insert(END, "100.0")
        duty_entry['state'] = 'disabled'
    else:
        duty_entry.insert(END, config["duty_cycle"])


def lock_rx_srate(rx_entry_widg, mode):
    rx_entry_widg['state'] = 'normal'
    rx_entry_widg.delete("0", END)
    if mode == 1:
        rx_entry_widg.insert(END, p.int2SI(int(config['rx_bandwidth']) * 2.4) + "Sps")
        rx_entry_widg['state'] = 'disabled'
    else:
        rx_entry_widg.insert(END, p.int2SI(int(config["rx_sample_rate"])) + "Sps")


def mutate_pdisp(entry_widg, mode):
    num = str(entry_widg.get())
    entry_widg.delete("0", END)
    if mode == "dBm":
        entry_widg.insert(END, str(Parser.watt2dbm(num)) + "dBm")
    else:
        entry_widg.insert(END, str(Parser.dbm2mWatt(Parser.get_first_num(num))))


def create_graph(_graph_frame):
    fig = plt.figure()
    grph = fig.subplots()

    dt = 0.01
    t = np.arange(0, 100000, dt)
    omega = 1000
    t_period = 10 ** 6 / int(config['sample_rate']) * int(config['num_samples'])
    v = np.sqrt(10 ** (float(config['pwr']) / 10) * 50 * 0.001)
    x = np.linspace(0, t_period, omega)
    nactive = t_period * (float(config['duty_cycle']) / 100) if config['tx_mode'] == 'pulse' else int(
        config['num_samples'])
    y = [v if i < nactive else 0 for i in x]
    y[0] = 0
    # Create a figure

    # Create graph
    grph.plot(x, y)
    grph.set_title('Output signal')
    grph.set_ylabel("Amplitude(V)")
    grph.set_xlabel("Time(us)")
    # Create two subplots and unpack the output array immediately

    canvas = FigureCanvasTkAgg(fig, master=_graph_frame)  # A tk.DrawingArea.
    canvas.get_tk_widget().place(rely=.0, relx=0, relheight=0.9, relwidth=1)
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, _graph_frame)
    toolbar.children['!button4'].pack_forget()
    toolbar.update()
    toolbar.place(rely=.90, relx=0, relheight=.1, relwidth=1)

    return fig


# Widget collections for easy access on Startup
entry_widgets = {}
radio_vars = {}

tab_win = ttk.Notebook(root_win)
tab1 = Frame(tab_win)
tab2 = Frame(tab_win)

tab_win.add(tab1, text="Power Beaming")
tab_win.add(tab2, text="Communications")

tab_win.pack(expand=1, fill='both')

# tab1.place(rely=.002, relheight=.996, relx=.001, relwidth=.998)
# tab2.place(rely=.002, relheight=.996, relx=.001, relwidth=.998)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Left Area Container Formatting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

left_container = Left_Design.Left_Area(tab1).area

basic_settings = Frame(left_container, bg="#afb0b3", relief=RAISED, borderwidth=1)
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

#########################
# Left area Comms
#########################

left_container2 = Left_Design.Left_Area(tab2).area
basic_settings2 = Frame(left_container2, bg="#afb0b3", relief=RAISED, borderwidth=1)
basic_settings2.place(rely=0, relx=0, relheight=0.49, relwidth=1)

freq_container2 = Frame(basic_settings2, bg="#afb0b3")
freq_container2.place(rely=0.01, relx=.01, height=70, relwidth=.52)

bw_container2 = Frame(basic_settings2, bg="#afb0b3")
bw_container2.place(y=75, relx=.01, height=70, relwidth=.52)

ch_ctrl_container2 = Frame(basic_settings2, bg="#afb0b3")
ch_ctrl_container2.place(y=150, relx=.01, height=70, relwidth=.52)

intermediate_settings2 = Frame(left_container2, bg="#afb0b3", relief=RAISED, borderwidth=1)
intermediate_settings2.place(rely=0.5, relx=0, relheight=1, relwidth=1)

rx_srate_container = Frame(intermediate_settings2, bg="#afb0b3")
rx_srate_container.place(y=5, relx=0, height=70, relwidth=.96)

rx_ns_container = Frame(intermediate_settings2, bg="#afb0b3")
rx_ns_container.place(y=75, relx=0, height=70, relwidth=.96)

rx_gain_container = Frame(intermediate_settings2, bg="#afb0b3")
rx_gain_container.place(y=150, relx=0, height=70, relwidth=.96)

# file_container2 = Frame(intermediate_settings2, bg="#afb0b3")
# file_container2.place(y=225, relx=.01, height=70, relwidth=.96)

# modulation_container = Frame(intermediate_settings2, bg="#afb0b3")
# modulation_container.place(y=150, relx=.01, height=70, relwidth=.96)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Right Area
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

text_font = font.Font(size=16)
right_area = Frame(tab1)
right_area.place(rely=0, relx=.48, relheight=.85, relwidth=.54)

output_win = ttk.Notebook(right_area)
text_frame = Frame(output_win)
graph_frame = Frame(output_win)

output_win.add(text_frame, text="Console")
output_win.add(graph_frame, text="Output Signal")

output_win.pack(expand=1, fill='both')
create_graph(graph_frame)

right_container = Frame(text_frame)
right_container.place(rely=.01, relx=.01, relheight=.97, relwidth=.94)

txt_o = Text(right_container, borderwidth=2, relief=SUNKEN)
txt_o.config(font=text_font, state="disabled")
txt_o.place(rely=0, relx=0, relheight=1, relwidth=1)

#########################
# Right area Comms
#########################
right_area2 = Frame(tab2)
right_area2.place(rely=0, relx=.48, relheight=.85, relwidth=.54)

output_win2 = ttk.Notebook(right_area2)
table_frame = Frame(output_win2)
text_frame2 = Frame(output_win2)
output_win2.add(table_frame, text="Actions")
output_win2.add(text_frame2, text="Console")
output_win2.pack(expand=1, fill='both')

actions_container = Frame(table_frame)
actions_container.place(rely=.01, relx=.01, relheight=.97, relwidth=.94)
txt_o2 = Text(text_frame2, borderwidth=2, relief=SUNKEN)
txt_o2.config(font=text_font, state="disabled")
txt_o2.place(rely=0, relx=0, relheight=1, relwidth=1)

Table.Table(actions_container)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Bottom Area
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
bottom_area = Frame(tab1)
bottom_area.place(rely=.85, relx=.48, relheight=.15, relwidth=.54)

button_font = font.Font(size=18)

help_label = Button(bottom_area, text="Help",
                    fg="white", bg="#4366d1", font=button_font, command=lambda: help_btn(txt_o, "help"))
help_label.place(rely=0.2, relx=0.05, relheight=.5, relwidth=.25)

ctrl_button = Button(bottom_area,
                     bg="#4366d1",
                     text="Stop" if running() else "Transmit",
                     fg="white", font=button_font,
                     command=lambda: start_ctrl(ctrl_button, txt_o))
ctrl_button.place(rely=.2, relx=0.35, relheight=.5, relwidth=.25)

quit_button = Button(bottom_area, bg="#4366d1", text="Quit to Desktop", fg="white", font=button_font,
                     command=lambda: root_win.destroy())
quit_button.place(rely=.2, relx=0.65, relheight=.5, relwidth=.29)

#########################
# Bottom area Comms
#########################
bottom_area2 = Frame(tab2)
bottom_area2.place(rely=.85, relx=.48, relheight=.15, relwidth=.54)

help_label2 = Button(bottom_area2, text="Help",
                     fg="white", bg="#4366d1", font=button_font, command=lambda: help_btn(txt_o2, "help"))
help_label2.place(rely=0.2, relx=0.05, relheight=.5, relwidth=.25)

ctrl_button2 = Button(bottom_area2,
                      bg="#4366d1",
                      text="Stop" if rx_running() else "Receive",
                      fg="white", font=button_font,
                      command=lambda: rx_ctrl(ctrl_button2, txt_o2))
ctrl_button2.place(rely=.2, relx=0.35, relheight=.5, relwidth=.25)

quit_button2 = Button(bottom_area2, bg="#4366d1", text="Quit to Desktop", fg="white", font=button_font,
                      command=lambda: root_win.destroy())
quit_button2.place(rely=.2, relx=0.65, relheight=.5, relwidth=.29)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Left Area Labels
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

label_font = font.Font(size=16)

basic_label = Label(basic_settings, text="Basic\nSettings", bg="#afb0b3", font=font.Font(size=25, weight="bold"),
                    fg="#f8f8f8")
basic_label.place(relx=0.62, rely=0.2)

freq_label = Button(freq_container, text="Frequency",
                    fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o, "freq"))
freq_label.place(rely=0.05, relx=0.05, height=70, width=145)

bw_label = Button(bw_container, text="Bandwidth",
                  fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o, "bw"))
bw_label.place(rely=0.05, relx=0.05, height=70, width=145)

ns_label = Button(sample_container, text="# Samples",
                  fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o, "num_samples"))
ns_label.place(rely=0.05, relx=0.025, relheight=.9, relwidth=.275)

sample_rate_label = Button(sample_container, text="Sample Rate",
                           fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o, "sample_rate"))
sample_rate_label.place(rely=0.05, relx=0.525, relheight=.9, relwidth=.275)

pwr_label = Button(pwr_container, text="Power",
                   fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o, "pwr"))
pwr_label.place(y=3.5, relx=0, height=63, relwidth=.275)

# gain_label = Button(gain_container, text="Gain",
#                     fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o, "gain"))
# gain_label.place(rely=0.05, relx=0.025, relheight=.9, relwidth=.275)

ch_mode_label = Button(ch_ctrl_container, text="Channel Mode",
                       fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o, "channel_mode"))
ch_mode_label.place(rely=0.05, relx=0.025, relheight=.9, relwidth=.275)

ch_label = Button(ch_ctrl_container, text="Channel",
                  fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o, "channel"))
ch_label.place(rely=0.05, relx=0.525, relheight=.9, relwidth=.275)

tx__mode_label = Button(tx_ctrl_container, text="Tx Mode",
                        fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o, "tx_mode"))
tx__mode_label.place(rely=0.05, relx=0.025, relheight=.9, relwidth=.275)

duty_label = Button(tx_ctrl_container, text="Duty Cycle",
                    fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o, "duty_cycle"))
duty_label.place(rely=0.05, relx=0.525, relheight=.9, relwidth=.275)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Left Area Controls
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ctrl_font = font.Font(size=15)

freq_widg = Entry(freq_container, bg="white", relief=SUNKEN, font=ctrl_font)
freq_widg.place(rely=0.14, x=173, height=50, width=140)
freq_widg.insert(END, p.int2SI(int(config['freq'])) + "Hz")
freq_widg.focus_set()
entry_widgets["freq"] = freq_widg

bw_widg = Entry(bw_container, bg="white", relief=SUNKEN, font=ctrl_font)
bw_widg.place(rely=0.14, x=173, height=50, relwidth=140)
bw_widg.insert(END, p.int2SI(int(config['bandwidth'])) + "Hz")
entry_widgets["bandwidth"] = bw_widg

ns_widg = Entry(sample_container, bg="white", relief=SUNKEN, font=ctrl_font)
ns_widg.place(rely=0.14, relx=.325, height=50, relwidth=.19)
ns_widg.insert(END, p.int2SI(int(config["num_samples"])))
entry_widgets["num_samples"] = ns_widg

sample_rate_widg = Entry(sample_container, bg="white", relief=SUNKEN, font=ctrl_font)
sample_rate_widg.place(rely=0.14, relx=.825, height=50, relwidth=.2)
sample_rate_widg.insert(END, p.int2SI(int(config["sample_rate"])))
entry_widgets["sample_rate"] = sample_rate_widg

pdisp_mode = StringVar(pwr_container, "dBm")
radio_vars["pwr_disp_mode"] = pdisp_mode
modes = {"Logarithmic": "dBm",
         "Linear": "W"}
for i, tup in enumerate(modes.items()):
    Radiobutton(pwr_container,
                text=tup[0],
                variable=pdisp_mode,
                value=tup[1],
                anchor='w',
                # label="Power Display"
                command=lambda: mutate_pdisp(entry_widg=pwr_widg, mode=pdisp_mode.get())
                ).place(y=3.5 + 31.5 * i, relx=.31, height=31.5, relwidth=.19)

pwr_widg = Entry(pwr_container, bg="white", relief=SUNKEN, font=ctrl_font)
pwr_widg.place(y=3.5, relx=.51, height=50, relwidth=.5)
pwr_widg.insert(END, p.int2SI(float(config["pwr"]), pdisp_mode.get()))
entry_widgets["pwr"] = pwr_widg

pwrI_label = Label(pwr_adv_tab, text="I",
                   fg="white", bg="#4366d1", font=label_font)
pwrI_label.place(y=3.5, relx=0, height=50, relwidth=.1)
pwr_adv_I = Entry(pwr_adv_tab, bg="white", relief=SUNKEN, font=ctrl_font)
pwr_adv_I.place(y=3.5, relx=.11, height=50, relwidth=.125)

pwrQ_label = Label(pwr_adv_tab, text="Q",
                   fg="white", bg="#4366d1", font=label_font)
pwrQ_label.place(y=3.5, relx=.25, height=50, relwidth=.1)
pwr_adv_Q = Entry(pwr_adv_tab, bg="white", relief=SUNKEN, font=ctrl_font)
pwr_adv_Q.place(y=3.5, relx=.36, height=50, relwidth=.125)

gain_label = Label(pwr_adv_tab, text="Gain",
                   fg="white", bg="#4366d1", font=label_font)
gain_label.place(y=3.5, relx=.5, height=50, relwidth=.125)
gain_entry = Entry(pwr_adv_tab, bg="white", relief=SUNKEN, font=ctrl_font)
gain_entry.place(y=3.5, relx=.635, height=50, relwidth=.125)

custom_display = Entry(pwr_adv_tab, bg="white", relief=SUNKEN, font=ctrl_font)
custom_display.place(y=70, relx=.425, height=50, relwidth=.9)
custom_label = Button(pwr_adv_tab, text="Custom Signal",
                      fg="white", bg="#4366d1", font=label_font,
                      command=lambda: custom_display.insert(END, tkinter.filedialog.askopenfilename()))
custom_label.place(y=70, relx=.0, height=50, relwidth=.4)

entry_widgets["pwr_i"] = pwr_adv_I

ch_mode = StringVar(ch_ctrl_container, config['channel_mode'])
radio_vars["channel_mode"] = ch_mode
modes = {"Single": "single",
         "MIMO": "mimo"}
for i, tup in enumerate(modes.items()):
    Radiobutton(ch_ctrl_container,
                text=tup[0],
                variable=ch_mode,
                value=tup[1],
                anchor='w',
                command=lambda: update(key='channel_mode', val=ch_mode.get(), txt_widg=txt_o)
                ).place(rely=0.05 + 0.45 * i, relx=.325, relheight=.45, relwidth=.19)

ch = IntVar(ch_ctrl_container, config['channel'])
radio_vars["channel"] = ch
modes = {"CH_1": "1",
         "CH_2": "2"}
for i, tup in enumerate(modes.items()):
    Radiobutton(ch_ctrl_container,
                text=tup[0],
                variable=ch,
                value=tup[1],
                anchor='w',
                command=lambda: update(key='channel', val=ch.get(), txt_widg=txt_o)
                ).place(rely=0.05 + 0.45 * i, relx=.825, relheight=.45, relwidth=.175)

tx_mode = StringVar(tx_ctrl_container, config['tx_mode'])
radio_vars["tx_mode"] = tx_mode
modes = {"Continuous": bladeRF_const.TxMode_CONTINUOUS,
         "Pulse": bladeRF_const.TxMode_PULSE}
for i, tup in enumerate(modes.items()):
    Radiobutton(tx_ctrl_container,
                text=tup[0],
                variable=tx_mode,
                value=tup[1],
                anchor='w',
                command=lambda: multi_func(lock_duty_cycle(duty_entry, tx_mode.get()),
                                           update(key='tx_mode', val=tx_mode.get(), txt_widg=txt_o),
                                           create_graph(graph_frame)
                                           )
                ).place(rely=0.05 + 0.45 * i, relx=.325, relheight=.45, relwidth=.19)

duty_entry = Entry(tx_ctrl_container, bg="white", relief=SUNKEN, font=label_font)
duty_entry.place(rely=0.14, relx=.825, height=50, relwidth=.175)
duty_entry.insert(END, config["duty_cycle"])
lock_duty_cycle(duty_entry, tx_mode.get())
entry_widgets["duty_cycle"] = duty_entry

#########################
# Left area Comm labels
#########################

basic_label2 = Label(basic_settings2, text="Basic\nSettings", bg="#afb0b3", font=font.Font(size=25, weight="bold"),
                     fg="#f8f8f8")
basic_label2.place(relx=0.62, rely=0.2)

freq_label2 = Button(freq_container2, text="Frequency",
                     fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o2, "rx_freq"))
freq_label2.place(rely=0.05, relx=0.05, height=70, width=145)

bw_label2 = Button(bw_container2, text="Bandwidth",
                   fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o2, "rx_bw"))
bw_label2.place(rely=0.05, relx=0.05, height=70, width=145)

ch_label2 = Button(ch_ctrl_container2, text="Channel",
                   fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o2, "channel"))
ch_label2.place(rely=0.05, relx=0.05, height=70, width=145)

sample_rate_label2 = Button(rx_srate_container, text="Sample Rate",
                            fg="white", bg="#4366d1", font=label_font,
                            command=lambda: help_btn(txt_o2, "rx_sample_rate"))
sample_rate_label2.place(rely=0.05, relx=0.04, relheight=.9, width=145)

rx_ns_label = Button(rx_ns_container, text="Number of\nSamples",
                     fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o2, "rx_sample_rate"))
rx_ns_label.place(rely=0.05, relx=0.04, relheight=.9, width=145)

gain_label = Button(rx_gain_container, text="Gain",
                    fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o2, "rx_gain"))
gain_label.place(rely=0.05, relx=0.04, relheight=.9, width=145)

# file_label = Button(file_container2, text="Output File\nLocation",
#                           fg="white", bg="#4366d1", font=('Arial', 14), command=lambda: help_btn(txt_o2, "rx_sample_rate"))
# file_label.place(rely=0.05, relx=0.05, relheight=.9, relwidth=.275)


# modulation_container = Button(modulation_container, text="Modulation",
#                           fg="white", bg="#4366d1", font=label_font, command=lambda: help_btn(txt_o, "sample_rate"))
# modulation_container.place(rely=0.05, relx=0.05, relheight=.9, relwidth=.275)

#########################
# Left area Comm Controls
#########################
freq_widg2 = Entry(freq_container2, bg="white", relief=SUNKEN, font=ctrl_font)
freq_widg2.place(rely=0.14, x=173, height=50, width=140)
freq_widg2.insert(END, p.int2SI(int(config['rx_freq'])) + "Hz")
entry_widgets["rx_freq"] = freq_widg2

bw_widg2 = Entry(bw_container2, bg="white", relief=SUNKEN, font=ctrl_font)
bw_widg2.place(rely=0.14, x=173, height=50, width=140)
bw_widg2.insert(END, p.int2SI(int(config['rx_bandwidth'])) + "Hz")
entry_widgets["rx_bandwidth"] = bw_widg2

rx_ch = IntVar(ch_ctrl_container2, config['rx_channel'])
radio_vars["rx_channel"] = ch
modes = {"CH_1": "1",
         "CH_2": "2"}
for i, tup in enumerate(modes.items()):
    Radiobutton(ch_ctrl_container2,
                text=tup[0],
                variable=rx_ch,
                value=tup[1],
                anchor='w',
                command=lambda: update(key='rx_channel', val=rx_ch.get(), txt_widg=txt_o2)
                ).place(rely=0.05 + 0.45 * i, relx=.6, relheight=.45, relwidth=.2)

rx_srate_entry = Entry(rx_srate_container, bg="white", relief=SUNKEN, font=ctrl_font)
rx_srate_entry.place(rely=0.13, relx=.48, height=50, relwidth=.19)
rx_srate_entry.insert(END, p.int2SI(int(config["rx_sample_rate"])))
entry_widgets["rx_sample_rate"] = rx_srate_entry
srate_mode = IntVar(rx_srate_container, config['auto'])
radio_vars["rx_channel"] = srate_mode
modes = {"Auto": "1",
         "Manual": "0"}
for i, tup in enumerate(modes.items()):
    Radiobutton(rx_srate_container,
                text=tup[0],
                variable=srate_mode,
                value=tup[1],
                anchor='w',
                command=lambda: multi_func(update(key='auto', val=srate_mode.get(), txt_widg=txt_o2),
                                           lock_rx_srate(rx_srate_entry, srate_mode.get()))
                ).place(rely=0.05 + 0.45 * i, relx=.33, relheight=.45, relwidth=.14)
lock_rx_srate(rx_srate_entry, srate_mode.get())

rx_ns_entry = Entry(rx_ns_container, bg="white", relief=SUNKEN, font=ctrl_font)
rx_ns_entry.place(rely=0.13, relx=.33, height=50, relwidth=.19)
rx_ns_entry.insert(END, p.int2SI(int(config["rx_num_samples"])))
entry_widgets["rx_ns"] = rx_ns_entry

rx_gain_entry = Entry(rx_gain_container, bg="white", relief=SUNKEN, font=ctrl_font)
rx_gain_entry.place(rely=0.14, relx=.33, height=50, relwidth=.19)
rx_gain_entry.insert(END, p.int2SI(int(config["rx_gain"])))

# file_widg = Entry(file_container2, bg="white", relief=SUNKEN, font=ctrl_font)
# file_widg.place(rely=0.14, relx=.35, height=50, relwidth=.19)
# file_widg.insert(END, p.int2SI(int(config["num_samples"])))
# datatype of menu text
# clicked = StringVar()
# initial menu text
# clicked.set("???")
# Create Dropdown menu
# drop = OptionMenu(modulation_container, clicked, *options)
# drop.place()

# Create button, it will change label text
# button = Button(modulation_container, text="click Me")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Callbacks
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

freq_widg.bind('<Return>', lambda e: entry_submit(e, "freq", txt_o))
freq_widg.bind('<FocusOut>', lambda e: entry_submit(e, "freq"))

bw_widg.bind('<Return>', lambda e: entry_submit(e, "bandwidth", txt_o))
bw_widg.bind('<FocusOut>', lambda e: entry_submit(e, "bandwidth", txt_o))

ns_widg.bind('<Return>', lambda e: multi_func(entry_submit(e, "num_samples", txt_o),
                                              create_graph(graph_frame)))
ns_widg.bind('<FocusOut>', lambda e: multi_func(entry_submit(e, "num_samples", txt_o),
                                                create_graph(graph_frame)))

duty_entry.bind('<Return>', lambda e: multi_func(entry_submit(e, "duty_cycle", txt_o),
                                                 create_graph(graph_frame)))
duty_entry.bind('<FocusOut>', lambda e: multi_func(entry_submit(e, "duty_cycle", txt_o),
                                                   create_graph(graph_frame)))

pwr_widg.bind('<Return>', lambda e: entry_submit(e, "pwr", txt_o))
pwr_widg.bind('<FocusOut>', lambda e: entry_submit(e, "pwr", txt_o))

sample_rate_widg.bind('<Return>', lambda e: multi_func(entry_submit(e, "sample_rate", txt_o),
                                                       create_graph(graph_frame)))
sample_rate_widg.bind('<FocusOut>', lambda e: multi_func(entry_submit(e, "sample_rate", txt_o),
                                                         create_graph(graph_frame)))

freq_widg2.bind('<Return>', lambda e: entry_submit(e, "freq", txt_o))
freq_widg2.bind('<FocusOut>', lambda e: entry_submit(e, "freq"))

bw_widg2.bind('<Return>', lambda e: entry_submit(e, "bandwidth", txt_o))
bw_widg2.bind('<FocusOut>', lambda e: entry_submit(e, "bandwidth", txt_o))

rx_ns_entry.bind('<Return>', lambda e: multi_func(entry_submit(e, "num_samples", txt_o),
                                                  create_graph(graph_frame)))
rx_ns_entry.bind('<FocusOut>', lambda e: multi_func(entry_submit(e, "num_samples", txt_o),
                                                    create_graph(graph_frame)))

rx_srate_entry.bind('<Return>', lambda e: multi_func(entry_submit(e, "num_samples", txt_o),
                                                     create_graph(graph_frame)))
rx_srate_entry.bind('<FocusOut>', lambda e: multi_func(entry_submit(e, "num_samples", txt_o),
                                                       create_graph(graph_frame)))

rx_gain_entry.bind('<Return>', lambda e: multi_func(entry_submit(e, "duty_cycle", txt_o),
                                                    create_graph(graph_frame)))
rx_gain_entry.bind('<FocusOut>', lambda e: multi_func(entry_submit(e, "duty_cycle", txt_o),
                                                      create_graph(graph_frame)))


################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
def recreate_win(left_area, left_container):
    left_container.destroy()
    left_container = Frame(left_area, bg="#afb0b3", borderwidth=1)
    left_container.place(rely=.01, relx=.01, relheight=.97, relwidth=.98)


# pwr_tab.bind("<<NotebookTabChanged>>", lambda e: recreate_win(left_area, left_container))

root_win.mainloop()
