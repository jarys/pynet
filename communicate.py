from errors import *
import pickle as pickle

class Packet:
    def __init__(self, data):
        self.data = data

def SendData(sock, data):
    #pickle data
    try:
        data = pickle.dumps(Packet(data))
        data = str(len(data)).encode() + b"||" + data
    except:
        sock.close()
        raise PickleError("The data could not be pickled.")
    #send data
    try:
        #print('sending', data)
        sock.send(data)
    except:
        sock.close()
        raise SocketError("Connection is broken; data could not be sent!")

def ReceiveData(sock):
    #receive data
    try:
        x = sock.recv(1024)
    except:
        sock.close()
        raise SocketError("Connection is broken; data could not be received!")
    #print('received', x)
    if not x:
        return 'None'
    n = x.split(b"||")[0]
    rest = x[len(n)+2::]
    size = int(n)
    buf = rest
    while len(buf) < size:
        try:
            buf += sock.recv(1024)
        except:
            sock.close()
            raise SocketError("Connection is broken; data could not be received!")

    #unpickle data
    try:
        data = pickle.loads(buf).data
        return data
    except:
        sock.close()
        raise PickleError("The data could not be unpickled.")


def send_one_message(sock, data):
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)

def recv_one_message(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
