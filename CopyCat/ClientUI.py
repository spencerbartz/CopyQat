from PIL import Image, ImageTk
from Tkinter import Tk, Text, RIGHT, BOTH, RAISED, X, Y, N, W, LEFT, Listbox, END
from ttk import Frame, Button, Style, Label, Entry

import ttk
import tkFont
import tkFileDialog

class ClientUI(Frame):
    def __init__(self):
        self.parent = Tk()
        Frame.__init__(self, self.parent)
        self.init_ui()
        self.file_queue = []
        self.file_opt = {}

    def init_ui(self):
        self.parent.title("Copy Qat")
        self.pack(fill = BOTH, expand = True)
        self.center_window()

        self.parent.attributes("-topmost", True)
        self.parent.focus_force()

        # osX requires this crap to focus a window
        import os
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

        self.style = Style()
        self.style.theme_use("aqua")

        # Create a frame for file list and attach to self
        file_frame = Frame(self, relief=RAISED, borderwidth=1)
        file_frame.pack(fill=X)

        fileLabel = Label(file_frame, text="Files", width=6)
        fileLabel.pack(side=LEFT, anchor=N, padx=5, pady=5)

        self.file_list = Listbox(file_frame)
        self.file_list.pack(side=LEFT, fill=BOTH, pady=5, padx=(0,50), expand=True)

        # Create a frame for buttons and attach to self
        button_frame = Frame(self)
        button_frame.pack(fill=BOTH)

        # Attach buttons to button_frame. padx can take a 2-tuple for left and right padding
        close_button = Button(button_frame, text="Exit", command=self.quit)
        close_button.pack(side=RIGHT, padx=(5, 50))
        send_button = Button(button_frame, text="Send Files")
        send_button.pack(side=RIGHT, padx=(5, 5))
        ok_button = Button(button_frame, text="Add File(s)", command=self.add_file_to_queue)
        ok_button.pack(side=RIGHT, padx=(5, 5))

    def center_window(self):
        width = 600
        height = 250

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - width) / 2
        y = (screen_height - height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def add_file_to_queue(self):
        file_opt_file = tkFileDialog.askopenfile(mode='r')
        self.file_queue.append(file_opt_file)
        self.file_list.insert(END, file_opt_file)

    def start(self):
        self.parent.mainloop()

if __name__ == '__main__':
     c = ClientUI()
     c.start()