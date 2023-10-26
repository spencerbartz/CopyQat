#############################################
#Server.py
#############################################

import socket
import os
import errno
import time
import sys
import threading

from CopyQat import MyUtil
from CopyQat import ClientHandler
from CopyQat import KennyLogger

class Server(threading.Thread):

    def __init__(self, save_dir = "CopyCatFiles", port = 8181, maxConn = 5):
        super(Server, self).__init__()

        self.save_dir = save_dir
        self.port = port
        self.maxConn = maxConn

        #Create / Locate the directory in which we will save received files
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self.kennyLogger = KennyLogger.KennyLogger()
        self.kennyLogger.initialize("server_logs");
        self.kennyLogger.logInfo("Starting Server")

        self.running = False
        self.clientHandlers = []
        self.setDaemon(True)

        #Create Server Socket and start listening
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(('', port))
        self.serversocket.listen(self.maxConn)
        self.running = True


    #################################################################
    # run()
    # Override of inherited method run() from threading.Thread
    # This method should not be called directly as it will be
    # invoked by Thread.start()
    # run starts the main server loop, listening for connections.
    # After a connection is received, a ClientHandler is created to
    # process the connection
    # @param self
    # @return None
    #################################################################
    def run(self):
        while self.running == True:
            self.kennyLogger.logInfo("Listening for connections")
            try:
                (clientsocket, address) = self.serversocket.accept()
                self.kennyLogger.logInfo("Accepted Connection from " + address[0] + " on port " + str(address[1]))

                newClient = ClientHandler.ClientHandler(clientsocket, self.save_dir, address)
                newClient.start()

                self.clientHandlers.append(newClient)

            except OSError as e:
                #most likely serversocket.close() was called by shutdown(), which also
                #sets self.running to false so we will not start listening for connections
                self.kennyLogger.logDebug("Handled OSError in main server loop " + str(e))
                pass


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
        self.kennyLogger.logInfo("Shutting Down")
        self.running = False;
        self.serversocket.close()
        for handler in self.clientHandlers:
            handler.join()


