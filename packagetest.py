from CopyCat import Client

import getopt
import sys

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


    #client = Client.Client()
    #client.readFile("testfile.txt")
    server = Server.Server()

if __name__ == "__main__":
    main()