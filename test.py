import client, server
import threading

s = server.Server()
s.connect('localhost', 8888)
threading.Thread(target=s.serve_forever).start()

c = client.Client()
c.connect('localhost', 8888)