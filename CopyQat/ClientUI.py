from PIL import Image, ImageTk
from Tkinter import Tk, Text, RIGHT, BOTH, RAISED, X, Y, N, W, LEFT, Listbox, END
from ttk import Frame, Button, Style, Label, Entry
from CopyCat import Client
import ttk
import tkFont
import tkFileDialog

class ClientUI(Frame):
    def __init__(self):
        self.parent = Tk()
        Frame.__init__(self, self.parent)
        self.init_ui()

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
        self.style.theme_use("default")

        # Create a frame for file list and attach to self
        file_frame = Frame(self, relief=RAISED, borderwidth=1)
        file_frame.pack(fill=X)

        # Create label and listbox and attach to file_frame
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
        send_button = Button(button_frame, text="Send Files", command=self.send_files)
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

    # Add the file name in string form to file_list
    def add_file_to_queue(self):
        file_opt_files = tkFileDialog.askopenfilenames()
        for f in file_opt_files:
            self.file_list.insert(END, f)

    def send_files(self):
        client = Client.Client()
        client.connect("127.0.0.1", 8181)
        file_names = list(self.file_list.get(0,self.file_list.size() - 1))
        client.open_files(file_names)
        client.read_files()
        client.send_files()

    def start(self):
        self.parent.mainloop()

if __name__ == '__main__':
     c = ClientUI()
     c.start()

