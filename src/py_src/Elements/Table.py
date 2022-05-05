from tkinter import *
import json
from tkinter.filedialog import askopenfilename


class Table:
    def __init__(self, root):
        with open("C:/Users/dkenn/Documents/XFORCE/Deliverables/PSDR/src/py_src/Elements/RxActions.json") as jfile:
            self.init_table = json.load(jfile)
        self.cols = self.init_table['columns']
        self.rows = self.init_table['rows']
        self.rowPopup = Popup(self)
        # code for creating table
        self.parent = root
        self.table_controls_frame = Frame(root, bg="green")
        self.table_controls_frame.pack()
        self.table_frame = None
        self.tableButton_add = Button(self.table_controls_frame, width=10, fg='black', text="+",
                                      font=('Arial', 16, 'bold'), command=self.add_row)
        self.tableButton_add.pack(side=LEFT)
        self.create_table()

    def create_table(self):
        self.update_table_info()
        if self.table_frame is not None:
            self.table_frame.destroy()
        self.table_frame = Frame(self.parent)
        self.table_frame.pack()
        # Make Header columns
        e = Entry(self.table_frame, width=10,
                  fg='white', bg='#afb0b3',
                  font=('Arial', 16, 'bold'), justify='center')
        e.grid(row=0, column=0, pady=(2.5, 2.5))
        e.insert(END, self.cols[0])
        e['disabledbackground'] = '#afb0b3'
        e['disabledforeground'] = 'white'
        e['state'] = 'disabled'

        e = Entry(self.table_frame, width=30,
                  fg='white', bg='#afb0b3',
                  font=('Arial', 16, 'bold'), justify='center')
        e.grid(row=0, column=1, pady=(2.5, 2.5))
        e.insert(END, self.cols[1])
        e['disabledbackground'] = '#afb0b3'
        e['disabledforeground'] = 'white'
        e['state'] = 'disabled'
        for i in range(0, len(self.rows)):
            self.make_row(i + 1, self.rows[i])

    def make_row(self, row, rowTup):
        e = Entry(self.table_frame, width=10,
                  fg='black',
                  font=('Arial', 16, 'bold'), justify='center')
        e.grid(row=row, column=0, pady=(2.5, 2.5))
        e.insert(END, rowTup[0]['value'])
        e['disabledbackground'] = 'white'
        e['disabledforeground'] = 'black'
        e['state'] = 'disabled'
        e = Entry(self.table_frame, width=30,
                  fg='black',
                  font=('Arial', 16, 'bold'),)
        e.grid(row=row, column=1, pady=(2.5, 2.5))
        e.insert(END, rowTup[1]['value'])
        e['disabledbackground'] = 'white'
        e['disabledforeground'] = 'black'
        e['state'] = 'disabled'
        e = Button(self.table_frame, fg='black',
                   font=('Arial', 11, 'bold'), text="edit",
                   command=lambda: self.rowPopup.edit_row(row - 1))
        e.grid(row=row, column=len(rowTup), padx=(2.5, 2.5))

        e = Button(self.table_frame, fg='black',
                   font=('Arial', 11, 'bold'), text="X",
                   command=lambda: self.del_row(row))
        e.grid(row=row, column=len(rowTup) + 1, padx=(2.5, 2.5))

    def update_table_info(self):
        with open("C:/Users/dkenn/Documents/XFORCE/Deliverables/PSDR/src/py_src/Elements/RxActions.json") as jfile:
            self.init_table = json.load(jfile)
            self.cols = self.init_table['columns']
            self.rows = self.init_table['rows']

    def add_row(self):
        if self.rowPopup.open is True:
            return
        self.rowPopup.new_row()

    def del_row(self, row):
        del self.init_table['rows'][row - 1]
        with open("C:/Users/dkenn/Documents/XFORCE/Deliverables/PSDR/src/py_src/Elements/RxActions.json", 'w') as jfile:
            json.dump(self.init_table, jfile, indent=2)
        self.create_table()


def get_ctrl(str):
    if str == "entry":
        return Entry()


class Popup:
    def __init__(self, table):
        self.open = False
        self.nameEntry = Entry()
        self.fileDiagEntry = Entry()
        self.parent_table = table

    def fileDiagUpdate(self):
        self.fileName = askopenfilename()

    def submit(self, row):
        if not isinstance(self.parent_table, Table):
            self.close()

        self.table_info['rows'][row][0]['value'] = self.nameEntry.get()
        self.table_info['rows'][row][1]['value'] = self.fileDiagEntry.get()
        with open("C:/Users/dkenn/Documents/XFORCE/Deliverables/PSDR/src/py_src/Elements/RxActions.json", 'w') as jfile:
            json.dump(self.table_info, jfile, indent=2)

        self.parent_table.create_table()
        self.close()

    def close(self):
        self.open = False
        self.win.destroy()

    def set_fileName(self, str):
        self.fileDiagEntry.insert(END, str)

    def new_row(self):
        with open("C:/Users/dkenn/Documents/XFORCE/Deliverables/PSDR/src/py_src/Elements/RxActions.json", 'r') as jfile:
            self.table_info = json.load(jfile)
        self.table_info['rows'].append([{"type": "entry", "value": ""},
                                        {"type": "entry", "value": ""}])
        self.openPopup(len(self.table_info['rows'])-1)

    def edit_row(self, row):
        with open("C:/Users/dkenn/Documents/XFORCE/Deliverables/PSDR/src/py_src/Elements/RxActions.json", 'r') as jfile:
            self.table_info = json.load(jfile)
        self.openPopup(row)

    def openPopup(self, row):
        if self.open:
            return
        self.open = True
        self.win = Toplevel()
        self.win.grab_set()

        # Set the geometry of Tkinter frame
        self.win.geometry("320x200")
        self.win.title("Add Command")
        self.win.protocol("WM_DELETE_WINDOW", self.close)

        titleWrapper = Frame(self.win)
        titleWrapper.place(x=10, y=35)
        actionWrapper = Frame(self.win)
        actionWrapper.place(x=10, y=70)
        submitWrapper = Frame(self.win)
        submitWrapper.place(x=0, y=140, relwidth=1)
        print(row)
        print(self.table_info)
        Label(titleWrapper, text="Name: ", font=('Arial', 16, 'bold')).pack(side=LEFT, padx=(5, 5.5))
        self.nameEntry = Entry(titleWrapper, width=14,
                               fg='black',
                               font=('Arial', 16, 'bold'))
        self.nameEntry.pack(side=LEFT)

        self.nameEntry.insert(END, self.table_info['rows'][row][0]['value'])

        Label(actionWrapper, text="Script: ", font=('Arial', 16, 'bold')).pack(side=LEFT, padx=(5, 5))
        self.fileDiagEntry = Entry(actionWrapper, width=14,
                                   fg='black',
                                   font=('Arial', 16, 'bold'))
        self.fileDiagEntry.pack(side=LEFT)
        self.fileDiagEntry.insert(END, self.table_info['rows'][row][1]['value'])
        Button(actionWrapper, width=2, fg='black', text="+",
               font=('Arial', 12, 'bold'), command=lambda: self.set_fileName(askopenfilename())).pack(side=LEFT,
                                                                                                      padx=(4, 0))

        Button(submitWrapper, width=10, fg='black', text="Submit",
               font=('Arial', 12, 'bold'), command=lambda: self.submit(row)).pack(side=BOTTOM)
