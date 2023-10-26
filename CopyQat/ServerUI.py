
from PIL import Image, ImageTk
from tkinter import Tk, Text, RIGHT, BOTH, RAISED, X, Y, N, W, LEFT, Listbox, END, font, filedialog
from tkinter.ttk import Frame, Button, Style, Label, Entry
import signal

from CopyQat import Server
from CopyQat import MyUtil
from CopyQat.MyUtil import *
from CopyQat import KennyLogger

class ServerUI(Frame):
    WIDTH = 480
    HEIGHT = 600

    # FUNCTION: __init__()
    # DESC: Initialize Tk, Begin this Frame's rendering loop
    # and initialize UI elements
    def __init__(self):
        self.parent = Tk()
        Frame.__init__(self, self.parent)
        self.init_ui()

    # FUNCTION: init_ui()
    # DESC: Create and center parent Frame (self), add labels, buttons
    # and list box for file names if multiple files are selected
    def init_ui(self):
        serverLogger = KennyLogger.KennyLogger()
        serverLogger.initialize("server_logs")
        serverLogger.logInfo("Initializing Server UI")

        # Add title and center this window
        self.parent.title("Copy Qat Server")
        self.pack(fill = BOTH, expand = True)
        center_window(self, self.WIDTH, self.HEIGHT)

        # Force window to come to highest z-index (-topmost) and grab focus
        self.parent.attributes("-topmost", True)
        self.parent.focus_force()
       
        # Set window and GUI look and feel
        self.parent.style = Style()
        self.parent.style.theme_use("clam")

        # Create frame for holding list of current connections
        conn_frame = Frame(self, relief=RAISED, borderwidth=1)
        conn_frame.pack(fill=X)

        # Create label & listbox, attach to file_frame
        conn_label = Label(conn_frame, text="User Connections", width=20)
        conn_label.pack(side=LEFT, anchor=N, padx=5, pady=20)

        self.file_list = Listbox(conn_frame, selectmode='extended')
        self.file_list.pack(side=LEFT, fill=BOTH, pady=20, padx=(0,50), expand=True)

        # Create frame for buttons and attach to self 
        button_frame = Frame(self)
        button_frame.pack(fill=BOTH)

        # ATTACH BUTTONS TO button_frame. Attach buttons to button_frame. padx CAN TAKE A 2-TUPLE FOR LEFT & RIGHT PADDING
        exit_button = Button(button_frame, text="Exit", command=self.quit)
        exit_button.pack(side=RIGHT, padx=(5, 50))
        run_button = Button(button_frame, text="Run Server", command=self.run_server)
        run_button.pack(side=RIGHT, padx=(5, 50))
        kick_button = Button(button_frame, text="Kick User", command=self.kick_user)
        kick_button.pack(side=RIGHT, padx=(5, 5))

    def run_server(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.server = Server.Server()        
        self.server.start()

    def signal_handler(self, signal, frame):
        self.server.running = False

    def kick_user(self):
        print("user kicked")

    # Start the Frame and in turn start the server
    def start(self):
        self.parent.mainloop()

if __name__ == '__main__':
     server_ui = ServerUI()
     server_ui.start()

