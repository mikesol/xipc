# xipc

Hackish experiment in interprocess communication.  It allows python to "call" javascript functions.

Check out [`py_calling.py`](./py_calling.py). It uses a library called [`xipc`](./xipc.py), which is in this repo. The top-level `with` statement "imports" four modules:

- [`py_called_1.py`](./py_called_1.py)
- [`py_called_2.py`](./py_called_2.py)
- [`js_called_1.js`](./js_called_1.js)
- [`js_called_2.js`](./js_called_2.js)

From python, we call all of the submethods.