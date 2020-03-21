#!/usr/local/bin/python3
# writer.py
import os
from message import create_msg

if __name__ == "__main__":
    IPC_FIFO_NAME = "hello_ipc"

    a = None
    with open('.pid', 'r') as x:
        a = int(x.read())
    fifo = os.fdopen(a, 'w')
    try:
        for _ in range(10000):
            name = "Mike"
            content = f"Hello {name}!".encode("utf8")
            msg = create_msg(content)
            os.write(fifo, msg)
    finally:
        os.close(fifo)