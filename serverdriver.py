from tkinter import *

from CopyQat import ServerUI
from CopyQat import KennyLogger

def main():
    # INITIALIZE AND START SERVER UI
    ui = ServerUI.ServerUI()
    ui.start()
  
    # INITIALIZE SINGLETON LOGGER
    serverLogger = KennyLogger.KennyLogger()
    serverLogger.initialize("server_logs")

if __name__ == "__main__":
    main()