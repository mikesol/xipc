import sys


def py_server(module: str, port: int) -> str:
    return """import socket
import json
import {module}

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = {port}        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        while True:
            ipt = 42
            data = conn.recv(1 << 16)
            data = data.decode('utf-8')
            fn = data.split(';')[0]
            if fn == '':
                break
            body = json.loads(';'.join(data.split(';')[1:]))
            func = getattr({module}, fn)
            res = func(*body)
            conn.sendall(json.dumps(res).encode('utf-8'))
""".format(
        module=module, port=port
    )


if __name__ == "__main__":
    print(py_server(sys.argv[1], int(sys.argv[2])))
