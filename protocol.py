import struct

def send(sock, data):
	length = len(data)
	sock.sendall(b'size' + struct.pack('!I', length) + data)

def recv(sock):
	protocol = sock.recv(8)
	if protocol[:4] == b'size':
		length, = struct.unpack('!I', protocol[4:])
		return recvall(sock, length)
	else:
		send(sock, b'Invalid protocol, send packet in form:' +
				   b' size[datalength(4bytes unsigned int)][data]')
		return b''

def recvall(sock, count):
	buf = b''
	while count:
		newbuf = sock.recv(count)
		if not newbuf: return None
		buf += newbuf
		count -= len(newbuf)
	return buf
