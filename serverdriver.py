import getopt
import sys
import signal

from CopyCat import Server
from CopyCat import KennyLogger

server = None
running = False

def main():
    
    kennyLogger = KennyLogger.KennyLogger()
    kennyLogger.initialize("serverlogs")
    
    saveFolder = "CopyCatFiles"
    port = 8181
    
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:p:", ["help", "savefolder", "port"])
    except getopt.GetOptError as msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)
        
    # process options
    for o, a in opts:
        if o in ("-h", "--help", "-help"):
            print("Example Usage: python serverdriver.py --savefolder c:\somepath\somefolder --port 8181")
            sys.exit(0)
        elif o in ("-s", "--savefolder", "-savefolder"):
            saveFolder = a
        elif o in ("-p", "--port", "-port"):
            port = int(a)


    signal.signal(signal.SIGINT, signal_handler)

    server = Server.Server(saveFolder, port)
    #TODO: this must raise some kind of exception we should be handling    
    server.start()
    running = True
        
    while running:
            try:
                userInput = input("Press Ctrl-c to exit\n")
            except (KeyboardInterrupt, EOFError):
                break

    server.shutdown()
    server.join()
    sys.exit(0)
                
def signal_handler(signal, frame):
    running = False

        
if __name__ == "__main__":
    main()