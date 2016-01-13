import socket,select,sys,time
from errors import *
import protocol
    
class Server():
    def __init__(self):
        self.sending_socket = None

    def input_func(self,sock,host,port,address):pass
    def output_func(self,sock,host,port,address):pass
    def connect_func(self,sock,host,port):print('server sucessfully bind')
    def client_connect_func(self,sock,host,port,address):print("client connected")
    def client_disconnect_func(self,sock,host,port,address):print("disconnecting client")
    def quit_func(self,host,port):print('server terminated')
        
    def connect(self, host, port):
        self.host = host
        self.port = port
        try:
            self.unconnected_socket = socket.socket()
            self.unconnected_socket.bind((self.host, self.port))
            self.unconnected_socket.listen(5)
            self.connect_func(self.unconnected_socket, self.host,self.port)
        except:
            self.unconnected_socket.close()
            raise ServerError("Only one instance of the server on port "+str(self.port)+" may run at one time!")
        self.connected_sockets = []
        self.socketaddresses = {}

    def remove_socket(self, sock):
        address = self.socketaddresses[sock]
        self.client_disconnect_func(sock, self.host, self.port, address)
        self.connected_sockets.remove(sock)

    def serve_forever(self):
        self.looping = True
        while self.looping:
            input_ready, output_ready, except_ready = select.select([self.unconnected_socket]+self.connected_sockets,[],[])
            for sock in input_ready:
                if sock == self.unconnected_socket:
                    #init socket
                    connected_socket, address = sock.accept()
                    self.connected_sockets.append(connected_socket)
                    self.socketaddresses[connected_socket] = address
                    self.client_connect_func(connected_socket, self.host, self.port, address)
                else:
                    data = protocol.recv(sock)
                    try:
                        address = self.socketaddresses[sock]
                        self.input_func(sock, self.host, self.port, address)
                    except:
                        data = b"client quit"
                    if data != None:
                        if data == b"client quit":
                            self.remove_socket(sock)
                        else:
                            self.sending_socket = sock
                            self.handle_data(data)
                    
    def handle_data(self, data):
        print("SERVER:", data)
        self.send_data_to_all(data)

    def send_data(self, data):
        try:
            protocol.send(self.sending_socket, data)
            address = self.socketaddresses[self.sending_socket]
            self.input_func(self.sending_socket,self.host,self.port,address)
        except:
            self.remove_socket(self.sending_socket)

    def send_data_to_all(self, data):
        for socket in self.connected_sockets:
            try:
                protocol.send(socket, data)
                address = self.socketaddresses[socket]
                self.input_func(socket,self.host,self.port,address)
            except:
                self.remove_socket(socket)
            
    def quit(self):
        for socket in self.connected_sockets:
            socket.close()

        self.quit_func(self.host, self.port)