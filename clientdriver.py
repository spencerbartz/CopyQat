from tkinter import *

from CopyQat import ClientUI
from CopyQat import KennyLogger

def main():
    # INITIALIZE AND START CLIENT UI
    ui = ClientUI.ClientUI()
    ui.start()
  
    # INITIALIZE SINGLETON LOGGER
    clientLogger = KennyLogger.KennyLogger()
    clientLogger.initialize("client_logs")

if __name__ == "__main__":
    main()