import socket
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    import time
    now = time.time()
    for x in range(10000):
        s.sendall(b'{"a":1,"b":2}')
        data = json.loads(s.recv(1024).decode('utf-8'))
    print(time.time() - now)