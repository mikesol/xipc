import time

from xipc import hack

with hack("py_called_1", "py_called_2", "js_called_1", "js_called_2") as mods:
    now = time.time()
    b = 0
    for x in range(1000):
        b += mods.py_called_1.add_ints(1, 2)  # type: ignore
    print("Time in seconds for 1000 additions using sockets:", time.time() - now)
    now = time.time()
    b = 0
    for x in range(1000):
        b += 1 + 2
    print("Time in seconds for 1000 additions:", time.time() - now)
