#############################################
#ClientHandler.py
#############################################
import threading
import os
import sys
import socket
import timeit
import logging

from CopyQat import MyUtil
from CopyQat import KennyLogger

class ClientHandler(threading.Thread):

    def __init__(self, clientsocket, saveDir, address):
        super(ClientHandler, self).__init__()
        self.clientsocket = clientsocket
        self.saveDir = saveDir
        self.address = address
        self.fileNames = []
        self.fileSizes = []
        self.kennyLogger = KennyLogger.KennyLogger()
        self.kennyLogger.logInfo("Started ClientHandler")


    #################################################################
    # run()
    # @return None
    #################################################################
    def run(self):

        self.kennyLogger.logInfo("Receiving File(s)")
        moreFiles = True

        while moreFiles == True:
            #get file names and sizes
            data = self.clientsocket.recv(2048).decode()

            if not data:
                moreFiles = False
                break

            (fileName, fileSize) = data.split(";")

            #open local file on server for writing
            outFile = open(self.saveDir + os.sep + fileName, "wb")

            #Tell the client we are ready to accept the file
            self.sendAck()

            #measure how long the file transfer takes
            startTime = timeit.default_timer()

            #Read the file contents and write to outfile
            totalRead = 0
            buffer = bytearray()
            while totalRead < int(fileSize):
                data = self.clientsocket.recv(min(int(fileSize) - totalRead, 8192))
                if not data:
                    self.kennyLogger.logError("Error: Failed to read from client")
                    moreFiles = False
                    break
                else:
                    outFile.write(data)
                    totalRead += len(data)
                    prin(fileName + "- PERCENT READ: " +  str(round(float(totalRead) / float(fileSize) * 100, 2)) + "%")

            #Tell the client the file was received and written
            self.sendAck()

            elapsed = timeit.default_timer() - startTime
            outFile.close()
            self.kennyLogger.logInfo("File Received: " + fileName + " (" + str(elapsed) + " seconds)")

        # Finished receiving file(s)
        self.kennyLogger.logInfo("Connection Closed: " + self.address[0] + " on port " + str(self.address[1]))
        self.clientsocket.close()

    #################################################################
    # sendAck()
    # @param String msg - message to send to the server
    # @return None
    #################################################################
    def sendAck(self):
        self.kennyLogger.logDebug("Sending Ack")
        sent = self.clientsocket.send("OK".encode())
        #print("sent ", sent)
        if sent == 0:
            self.kennyLogger.logError("Could not send ack to client")
            raise RuntimeError("socket connection broken")

