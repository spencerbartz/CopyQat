from CopyCat import Client

import getopt
import sys

def main():
    
    file = None
    
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
            print("Example Usage: python clientdriver.py somefile.txt")
            sys.exit(0)
        elif o in ("-f", "--file"):
            file = a
            
    # process arguments
    for arg in args:
        print(arg) # process() is defined elsewhere


    client = Client.Client()
    client.connect("127.0.0.1", 8181)
    
    if file is None:
        client.readFile("testfile.txt")
    else:
        client.readFile(file)
    
    client.sendFile()


if __name__ == "__main__":
    main()