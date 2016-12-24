from PIL import Image, ImageTk
from Tkinter import Tk, Text, RIGHT, BOTH, RAISED, X, Y, N, W, LEFT, Listbox, END
from ttk import Frame, Button, Style, Label, Entry

import ttk
import tkFont

class ClientUI(Frame):

    def __init__(self):
        self.parent = Tk()
        Frame.__init__(self, self.parent)
        self.initUI()

    def initUI(self):
        self.parent.title("Copy Qat")
        self.pack(fill = BOTH, expand = True)
        self.centerWindow()

        self.parent.attributes("-topmost", True)
        self.parent.focus_force()

        # osX requires this crap to focus a window
        import os
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

        self.style = Style()
        self.style.theme_use("aqua")

        fileFrame = Frame(self, relief=RAISED, borderwidth=1)
        fileFrame.pack(fill=X)

        fileLabel = Label(fileFrame, text="Files", width=6)
        fileLabel.pack(side=LEFT, anchor=N, padx=5, pady=5)

        fileList = Listbox(fileFrame)
        fileList.pack(side=LEFT, fill=BOTH, pady=5, padx=(0,50), expand=True)

        buttonFrame = Frame(self)
        buttonFrame.pack(fill=BOTH)

        # padx can take a 2-tuple for left and right padding
        closeButton = Button(buttonFrame, text="Exit", command=self.quit)
        closeButton.pack(side=RIGHT, padx=(5, 50))
        sendButton = Button(buttonFrame, text="Send Files", command=self.quit)
        sendButton.pack(side=RIGHT, padx=(5, 5))
        okButton = Button(buttonFrame, text="Add File(s)")
        okButton.pack(side=RIGHT, padx=(5, 5))

    def centerWindow(self):
        width = 600
        height = 250

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - width) / 2
        y = (screen_height - height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))


    def start(self):
        self.parent.mainloop()

# if __name__ == '__main__':
#     main()