import json
import logging
import os
import socket
import subprocess
from dataclasses import dataclass
from typing import Any, Sequence

logger = logging.getLogger(__name__)


class xipc:
    pass


def mod(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", port))

    class _mod:
        def __getattribute__(self, name: str) -> Any:
            def callable(*args):
                argz = json.dumps(args)
                s.sendall((name + ";" + argz).encode("utf-8"))
                return json.loads(s.recv(2048).decode("utf-8"))

            return callable

    return _mod(), s


class xipc:
    start_port = 8001
    end_port = 8001

    def __init__(self, *scripts: str):
        self._scripts = scripts
        self._sox = []

    def __enter__(self):
        logger.debug("starting xipc")
        port = self.start_port
        out = xipc()
        dr = os.listdir(".")
        self._sox = []
        for script in self._scripts:
            if ("%s.py" % script) in dr:
                fn = ".xipc.%d.py" % port
                with open(fn, "w") as fi:
                    fi.write(
                        subprocess.check_output(
                            ["python", "py_server.py", script, str(port)]
                        ).decode("utf-8")
                    )
                    subprocess.Popen(
                        ["python", fn],
                        stderr=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                    )
            elif ("%s.js" % script) in dr:
                fn = ".xipc.%d.js" % port
                with open(fn, "w") as fi:
                    fi.write(
                        subprocess.check_output(
                            ["python", "js_server.py", script, str(port)]
                        ).decode("utf-8")
                    )
                    subprocess.Popen(
                        ["node", fn],
                        stderr=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                    )
            else:
                raise ValueError("Cannot handle %s" % script)
            modl, sok = mod(port)
            self._sox.append(sok)
            setattr(out, script, modl)
            port += 1
        self.end_port = port
        return out

    def __exit__(self, type, value, traceback):
        for s in self._sox:
            s.sendall(";".encode("utf-8"))
            s.close()
