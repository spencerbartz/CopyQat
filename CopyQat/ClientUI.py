
from PIL import Image, ImageTk
from tkinter import Tk, Text, RIGHT, BOTH, RAISED, X, Y, N, W, LEFT, Listbox, END, font, filedialog
from tkinter.ttk import Frame, Button, Style, Label, Entry

from CopyQat import Client
from CopyQat import MyUtil
from CopyQat.MyUtil import *

class ClientUI(Frame):
    # CONSTRUCTOR
    def __init__(self):
        self.parent = Tk()
        Frame.__init__(self, self.parent)
        self.init_ui()

    # INITIALIZE UI: WINDOW, LABELS, BUTTONS, FILE NAME LIST BOX
    def init_ui(self):
        # DRAW WINDOW AND TITLE
        self.parent.title("Copy Qat")
        self.pack(fill = BOTH, expand = True)
        center_window(self, 600, 250)

        self.parent.attributes("-topmost", True)
        self.parent.focus_force()
       
        self.style = Style()
        self.style.theme_use("default")

        # CREATE A FRAME FOR FILE LIST AND ATTACH TO SELF
        file_frame = Frame(self, relief=RAISED, borderwidth=1)
        file_frame.pack(fill=X)

        # CREATE LABEL & LISTBOX AND ATTACH TO file_frame
        file_label = Label(file_frame, text="Files", width=6)
        file_label.pack(side=LEFT, anchor=N, padx=5, pady=5)

        self.file_list = Listbox(file_frame, selectmode='extended')
        self.file_list.pack(side=LEFT, fill=BOTH, pady=5, padx=(0,50), expand=True)

        # CREATE A FRAME FOR BUTTONS & ATTACH TO SELF
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
     c = ClientUI()
     c.start()

