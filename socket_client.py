import json
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8003  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    import time

    now = time.time()
    for x in range(10000):
        s.sendall(b"add_ints;[1,2]")
        data = s.recv(1024).decode("utf-8")
        data = json.loads(data)
    print(time.time() - now)
