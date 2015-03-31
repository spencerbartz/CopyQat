from CopyCat import Server

import getopt
import sys
import signal

server = None
running = False

def main():
    
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:v", ["help", "file"])
    except getopt.GetOptError as msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)
        
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print("something helpful")
            sys.exit(0)
            
    # process arguments
    for arg in args:
        print(arg) # process() is defined elsewhere


    signal.signal(signal.SIGINT, signal_handler)

    server = Server.Server()
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