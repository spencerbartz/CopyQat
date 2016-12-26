#############################################
#CLient.py
#############################################
import socket
import os
import signal
import sys
import timeit
import inspect

from CopyQat import KennyLogger

class Client:

    def __init__(self, sock = None):

        self.kennyLogger = KennyLogger.KennyLogger()
        self.kennyLogger.initialize()

        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        self.file_objects = []
        self.file_contents = []
        self.fileInfo = ""


    #################################################################
    # connect()
    # @param msg
    # @return None
    #################################################################
    def connect(self, host, port):
        self.sock.connect((host, port))

    #################################################################
    # send_files()
    # @param msg
    # @return None
    #################################################################
    def send_files(self):
        if self.file_objects == []:
            self.kennyLogger.logError("Error, file object list was empty")
            return

        if self.file_contents == []:
            print("Error file contents list was empty")
            return

        for file_obj, file_text in zip(self.file_objects, self.file_contents):
                file_size = len(file_text)

                #send the server the file name and file size we want to send
                self.send_msg(os.path.basename(file_obj.name) + ";" + str(file_size))

                #receive the OK from the server
                if self.recv_ack() == False:
                    print("File '", file_obj.name, "' not sent. Could not get acknowledgement from server")
                    return

                #Windows does something strange where the os.fstat file size may be larger than the actual number of
                #bytes available to be read, so we won't use this: < os.fstat(self.file_object.fileno()).st_size >
                file_size = len(file_text)
                total_sent = 0

                start_time = timeit.default_timer()
                while total_sent < file_size:
                    sent = self.sock.send(file_text[total_sent:])
                    if sent == 0:
                        raise RuntimeError("socket connection broken")
                    total_sent = total_sent + sent

                if self.recv_ack() == True:
                    self.kennyLogger.logInfo("File sent successfully")
                else:
                    self.kennyLogger.warn("File was sent but no ack from server")
                elapsed = timeit.default_timer() - start_time
                self.kennyLogger.logInfo("Total bytes sent: " + str(total_sent) + " (" + str(elapsed) + " seconds)")

    #################################################################
    # send_msg()
    # @param String msg - message to send to the server
    # @return None
    #################################################################
    def send_msg(self, msg):
        total_sent = 0

        while total_sent < len(msg):
            sent = self.sock.send(msg[total_sent:].encode())
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent

    #################################################################
    # read_files()
    # @param
    # @return None
    #################################################################
    def read_files(self):
        for file_obj in self.file_objects:
            contents = file_obj.read()
            self.file_contents.append(contents)


    #################################################################
    # open_files()
    # @param String file_names - Semicolon delimited list of file names
    # @return None
    #################################################################
    def open_files(self, file_names):
        for file_name in file_names:
            file = open(file_name, "rb")
            self.kennyLogger.logInfo("Opened file: " + file.name)
            self.file_objects.append(file)

    #################################################################
    # recv_ack()
    # @param
    # @return None
    #################################################################
    def recv_ack(self):

        chunks = []
        bytes_recd = 0

        while bytes_recd < 2:
            chunk = self.sock.recv(2)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

        Ack = (b''.join(chunks)).decode()

        if Ack == "OK":
            return True;
        else:
            print("ACK NOT OK")
            return False
