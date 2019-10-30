from tkinter import *

import getopt
import sys

from CopyQat import ClientUI
from CopyQat import KennyLogger

def main():
    # INITIALIZE AND START CLIENT UI
    ui = ClientUI.ClientUI()
    ui.start()
  
    # INITIALIZE SINGLETON LOGGER
    kennyLogger = KennyLogger.KennyLogger()
    kennyLogger.initialize("clientlogs")

if __name__ == "__main__":
    main()