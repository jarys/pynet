import socket,select,sys,time
import protocol

class Client:
    def connect(self, host, port):
        self.host = host
        self.port = port
        try:
            self.sock = socket.socket()
            self.sock.connect((self.host, self.port))
        except:
            self.sock.close()
            raise
        
    def send(self, data):
        protocol.send(self.sock, data)

    def recv(self):
        return protocol.recv(self.sock)
    
    def quit(self):
        protocol.send(self.sock, b"client quit")
        self.sock.close()
