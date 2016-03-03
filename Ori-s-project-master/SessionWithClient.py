import threading
import socket
#from MyCrypto import * 

ERROR_SOCKET = "Socket_Error"
END_LINE = "\r\n"
LEN_UNIT_BUF = 2048
ERROR_EXCEPT = "Exception"


class SessionWithClient(threading.Thread):
    aes_key = None

    def __init__(self, pythonServer, clientSock, addr ):
        threading.Thread.__init__(self)
        # reference to parent server
        self.pythonServer = pythonServer
        # new open socket  for client
        self.clientSock = clientSock
        # address connection : IP and Port
        self.addr = addr

    def send(self, data):
        self.pythonServer.crypto_object.send_data(self.aes_key, self.clientSock, data)

    def recv_buf(self):
        return self.pythonServer.crypto_object.recv_data(self.aes_key, self.clientSock)


    def run(self):
        while True:
            try:
                if self.pythonServer.startFlag:
                    pass
            except socket.error , e:
                print str(e) + END_LINE + ERROR_SOCKET
                continue
            except Exception as e:
                print str(e) + END_LINE + ERROR_EXCEPT   
                continue

    def print_log_message(self, message):
        # Print to GUI
        self.pythonServer.gui.guiSock.send(message + "#")

