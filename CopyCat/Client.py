#############################################
#CLient.py
#############################################
import socket
import os
import signal
import sys

class Client:
    
    def __init__(self, sock = None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
    
        self.fileObject = None
    
    
    def connect(self, host, port):
        self.sock.connect((host, port))

    def sendFile(self):
        
        if self.fileObject is None:
            print("Error, file not initialized")
            return
        else:
            fileSize = len(self.fileText)
            
            self.sendMsg(self.fileObject.name + ";" + str(fileSize))

            fileSize = len(self.fileText) #os.fstat(self.fileObject.fileno()).st_size
            
            print(fileSize)
            totalsent = 0
            
            while totalsent < fileSize:
                print("sending data...")
                sent = self.sock.send(self.fileText[totalsent:])
                print("sent ", sent)
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent
                
    def sendMsg(self, msg):
            totalsent = 0
            while totalsent < len(msg):
                sent = self.sock.send(msg[totalsent:].encode())
                
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)
    
    def readFile(self, fileName):
        #fileName = input("Enter file name: ")
        #print("Received input is : ", fileName)
        
        self.fileObject = open(fileName, "rb")
        self.fileText = self.fileObject.read()
        
        print("strlen of file text ", len(self.fileText))
        
        #print("File Text: " , fileText)
    
    
    