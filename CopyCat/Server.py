#############################################
#Server.py
#############################################

import socket
import os
import errno
import time
import sys
import threading

from CopyCat import MyUtil

class Server(threading.Thread):

    def __init__(self, serverSock = None, port = 8181, numConn = 5, saveDir = "CopyCatFiles"):
        super(Server, self).__init__()
        print("Starting Up...")

        self.running = False
        self.saveDir = saveDir
        self.setDaemon(True)
        
        #Create Server Socket and start listening
        if serverSock is None:
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serversocket.bind(("127.0.0.1", port))
            self.serversocket.listen(numConn)
            self.running = True
        else:
            self.serverSocket = serverSock
            
        #Create / Locate the directory in which we will save received files
        if not os.path.exists(self.saveDir):
            os.makedirs(self.saveDir)
            
        
    def run(self):
        while self.running == True:
            print("Listening...")
            try:
                (clientsocket, address) = self.serversocket.accept()
                print("Accepted Connection from ", address)
                
            
                #get file name and size
                data = clientsocket.recv(1024).decode()
                if not data:
                    print("Error: Failed to read from client")
                    return
                else:
                    (fileName, fileSize) = data.split(";")
                    print("FILENAME: " + fileName + " FILE SIZE: " + fileSize)
                    print("Save dir: " + self.saveDir + os.sep + fileName)
                    outFile = open(self.saveDir + os.sep + fileName, "wb")
                    
                    totalRead = 0
                    while totalRead < int(fileSize):
                        data = clientsocket.recv(1024)
                        if not data:
                            print("Error: Failed to read from client")
                            return
                        else:
                            outFile.write(data)
                            totalRead += len(data)
                            print("total read ", totalRead)
                    print("finished reading file: ", fileName)
                    outFile.close()
                    
                clientsocket.close()            
            except OSError as e:
                #most likely serversocket.close was called by shutdown()
                pass
                #print(e)
                #print("Listening Interrupted")
        #print("Exited main server loop")
                        
    #################################################################
    # shutdown()
    # Shuts down the server. Just setting "running" to False is not
    # enough to break the blocking call made by accept(), therefore
    # after we set "running" to false, we interrupt the call to
    # serversocket.accept() by calling close, which will raise an
    # OSError (WinError 10004 on Win 8.1), which we catch and ignore
    # then causing the while loop to execute again. With running set
    # to false the condition will fall through and the run() method
    # will exit, thus completing the server thread. The class that
    # instantiates a Server object is responsible for calling .join()
    # to ensure the thread has run to completion.
    #################################################################  
    @MyUtil.synchronized_method              
    def shutdown(self):
        print("Shutting Down")
        self.running = False;
        self.serversocket.close()
    

