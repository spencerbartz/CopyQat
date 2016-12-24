from Tkinter import *

import getopt
import sys

from CopyCat import ClientUI
from CopyCat import KennyLogger

def main():
    ui = ClientUI.ClientUI()
    ui.start()

    # file = "testfile.txt"
    # serverIP = "127.0.0.1"
    # serverPort = 8181
    #
    kennyLogger = KennyLogger.KennyLogger()
    kennyLogger.initialize("clientlogs")
    #
    # # parse command line options
    # try:
    #     opts, args = getopt.getopt(sys.argv[1:], "hf:i:p:", ["help", "file=", "ip=", "port="])
    # except getopt.GetOptError as errMsg:
    #     print(errMsg)
    #     print("for help use --help")
    #     sys.exit(2)
    #
    # # process options
    # for o, a in opts:
    #     if o in ("-h", "--help", "-help"):
    #         print("Example Usage: python clientdriver.py --file somefile.txt --ip 127.0.0.1 --port 8181")
    #         sys.exit(0)
    #     elif o in ("-f", "--file", "-file"):
    #         file = a
    #     elif o in ("-i", "--ip", "-ip"):
    #         serverIP = a
    #     elif o in ("-p", "--port", "-port"):
    #         serverPort = int(a)
    #     else:
    #         assert False, "Unhandled Option"
    #
    # client = Client.Client()
    # try:
    #     client.connect(serverIP, serverPort)
    # except ConnectionRefusedError:
    #     print("The server at <", serverIP, "> on port <", serverPort, "> is not running.")
    #     kennyLogger.error("Failed to connect to server. IP: " + serverIP + " port: " + str(serverPort))
    #     sys.exit(1)
    #
    # client.open_files(file)
    # client.readFiles()
    # client.sendFiles()


if __name__ == "__main__":
    main()