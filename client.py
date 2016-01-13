import socket,select,sys,time
from errors import *
from communicate import SendData, ReceiveData

class Client:
    def __init__(self):
        pass
    def connect(self, host, port):
        self.host = host
        self.port = port
        try:
            self.sock = socket.socket()
            self.sock.connect((self.host, self.port))
        except:
            self.sock.close()
            raise SocketError("The connection could not be opened.  It must be created first with a server object.")
        
    def send_data(self, data):
        SendData(self.sock, data)
    def receive_data(self):
        data = ReceiveData(self.sock)
        return data
    
    def quit(self):
        SendData(self.sock, b"client quit")
        self.sock.close()
