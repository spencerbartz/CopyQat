#############################################
#CLient.py
#############################################
import socket
import os
import signal
import sys
import timeit
import inspect

from CopyCat import KennyLogger

class Client:
    
    def __init__(self, sock = None):
        
        self.kennyLogger = KennyLogger.KennyLogger()
        
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
    
        self.fileObjects = []
        self.fileContents = []
        self.fileInfo = ""
    
    
    #################################################################
    # connect()
    # @param msg
    # @return None
    ################################################################# 
    def connect(self, host, port):
        self.sock.connect((host, port))

    #################################################################
    # sendFiles()
    # @param msg
    # @return None
    ################################################################# 
    def sendFiles(self):
        
        if self.fileObjects == []:
            self.kennyLogger.logError("Error, file object list was empty")
            return
        
        if self.fileContents == []:
            print("Error file contents list was empty")
            return
        
        for fileObj, fileText in zip(self.fileObjects, self.fileContents):
                fileSize = len(fileText)
                
                #send the server the file name and file size we want to send
                self.sendMsg(fileObj.name + ";" + str(fileSize))
                
                #receive the OK from the server
                if self.recvAck() == False:
                    print("File '", fileObj.name, "' not sent. Could not get acknowledgement from server")
                    return
    
                #Windows does something strange where the os.fstat file size may be larger than the actual number of
                #bytes available to be read, so we won't use this: < os.fstat(self.fileObject.fileno()).st_size >
                fileSize = len(fileText) 
                
                #print(fileSize)
                totalsent = 0
                
                startTime = timeit.default_timer()
                while totalsent < fileSize:
                    #print("sending data...")
                    sent = self.sock.send(fileText[totalsent:])
                    #print("sent ", sent)
                    if sent == 0:
                        raise RuntimeError("socket connection broken")
                    totalsent = totalsent + sent
                 
                if self.recvAck() == True:
                    self.kennyLogger.logInfo("File sent successfully")
                else:
                    self.kennyLogger.warn("File was sent but no ack from server")
                elapsed = timeit.default_timer() - startTime
                self.kennyLogger.logInfo("Total bytes sent: " + str(totalsent) + " (" + str(elapsed) + " seconds)")
            
    #################################################################
    # sendMsg()
    # @param String msg - message to send to the server
    # @return None
    #################################################################                
    def sendMsg(self, msg):
        
        totalsent = 0
        
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:].encode())
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        
    #################################################################
    # readFiles()
    # @param
    # @return None
    #################################################################  
    def readFiles(self):
        
        for fileObj in self.fileObjects:
            #self.fileInfo.join(fileObj.name + ";")
            
            contents = fileObj.read()
            
            #self.fileInfo.join(str(len(contents)) + ";")
            
            self.fileContents.append(contents)
    
    
    #################################################################
    # openFiles()
    # @param String fileNames - Semicolon delimited list of file names
    # @return None
    #################################################################  
    def openFiles(self, fileNames):
        
        fileNames = fileNames.split(";")
        
        for fileName in fileNames:
            file = open(fileName, "rb")
            self.kennyLogger.logInfo("Opened file: " + str(file))
            self.fileObjects.append(file)
            
        
    #################################################################
    # recvAck()
    # @param
    # @return None
    #################################################################   
    def recvAck(self):
        
        chunks = []
        bytes_recd = 0
        
        while bytes_recd < 2:
            chunk = self.sock.recv(2)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        
        Ack = (b''.join(chunks)).decode()
        
        #print("ACK", Ack)

        if Ack == "OK":
            return True;
        else:
            print("ACK NOT OK")
            return False
    