
from PIL import Image, ImageTk
from tkinter import Tk, Text, RIGHT, BOTH, RAISED, X, Y, N, W, LEFT, Listbox, END, font, filedialog, Menu
from tkinter.ttk import Frame, Button, Style, Label, Entry

from CopyQat import Client
from CopyQat import MyUtil
from CopyQat.MyUtil import *

class ClientUI(Frame):
    WIDTH = 600
    HEIGHT = 250

    # FUNCTION: __init__()
    # DESC: Initialize Tk, Begin this Frame's rendering loop
    # and initialize UI elements
    def __init__(self):
        self.parent = Tk()
        Frame.__init__(self, self.parent)
        self.init_ui()

    # Menu action handler functions
    def help(self):
        print("help()")

    def about(self):
        print("about()")

    def new_item(self):
        print("new()")

    def open(self):
        print("new()")

    def save(self):
        print("save()")

    def file_item(self):
        print("file_item()")

    # FUNCTION: init_ui()
    # DESC: Create and center parent Frame (self), add labels, buttons
    # and list box for file names if multiple files are selected
    def init_ui(self):
   
        menubar = Menu(self.parent)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_item)
        filemenu.add_command(label="Open", command=self.open)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.parent.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.help)
        helpmenu.add_command(label="About...", command=self.about)

        # Add the options to the menu 
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.parent.config(menu=menubar)
        # self.parent.mainloop()

        # create a toplevel menu
        menubar = Menu(self.parent)
        menubar.add_command(label="File", command=self.file_item)
        menubar.add_command(label="Exit", command=self.parent.quit)

        # display the menu
        self.parent.config(menu=menubar)

        # Add title and center this window
        self.parent.title("Copy Qat Client")
        self.pack(fill = BOTH, expand = True)
        center_window(self, self.WIDTH, self.HEIGHT)

        # Force window to come to highest z-index (-topmost) and grab focus
        self.parent.attributes("-topmost", True)
        self.parent.focus_force()
       
        # Set window and GUI look and feel
        self.parent.style = Style()
        self.parent.style.theme_use("clam")

        # Create frame for holding file list and add
        file_frame = Frame(self, relief=RAISED, borderwidth=1)
        file_frame.pack(fill=X)

        # Create label & listbox, attach to file_frame
        file_label = Label(file_frame, text="Files", width=6)
        file_label.pack(side=LEFT, anchor=N, padx=5, pady=5)

        self.file_list = Listbox(file_frame, selectmode='extended')
        self.file_list.pack(side=LEFT, fill=BOTH, pady=5, padx=(0,50), expand=True)

        # Create frame for buttons and attach to self 
        button_frame = Frame(self)
        button_frame.pack(fill=BOTH)

        # ATTACH BUTTONS TO button_frame. Attach buttons to button_frame. padx CAN TAKE A 2-TUPLE FOR LEFT & RIGHT PADDING
        close_button = Button(button_frame, text="Exit", command=self.quit)
        close_button.pack(side=RIGHT, padx=(5, 50))
        remove_button = Button(button_frame, text="Remove Files", command=self.remove_files)
        remove_button.pack(side=RIGHT, padx=(5, 5))
        send_button = Button(button_frame, text="Send Files", command=self.send_files)
        send_button.pack(side=RIGHT, padx=(5, 5))
        ok_button = Button(button_frame, text="Add File(s)", command=self.add_file_to_queue)
        ok_button.pack(side=RIGHT, padx=(5, 5))

    def remove_files(self):
        # Remove files in reverse order since deletion changes the indices
        # of selected items. (I.e. delete 0th item -> 1st item becomes 0th item)
        indices = list(self.file_list.curselection())
        indices.reverse()
        for i in indices:
            self.file_list.delete(i)

    def send_files(self):
        client = Client.Client()
        client.connect("127.0.0.1", 8181)

        selected_indices = list(self.file_list.curselection())
        all_files = list(self.file_list.get(0, self.file_list.size() - 1))
        selected_files = [all_files[i] for i in selected_indices]

        client.open_files(selected_files)
        client.read_files()
        client.send_files()
        self.remove_files()

    # ADD THE FILE NAME IN STRING FORM TO file_list
    def add_file_to_queue(self):
        file_opt_files = filedialog.askopenfilenames()
        for f in file_opt_files:
            self.file_list.insert(END, f)

    # BEGIN RUNNING THE FRAME
    def start(self):
        self.parent.mainloop()

if __name__ == '__main__':
     client_ui = ClientUI()
     client_ui.start()

