# xipc

Hackish experiment in interprocess communication.  It allows Python to "call" JavaScript functions.

Check out [`py_calling.py`](./py_calling.py). It uses a library called [`xipc`](./xipc.py), which is in this repo. The top-level `with` statement "imports" four modules:

- [`py_called_1.py`](./py_called_1.py)
- [`py_called_2.py`](./py_called_2.py)
- [`js_called_1.js`](./js_called_1.js)
- [`js_called_2.js`](./js_called_2.js)

Then, it calls a bunch of functions. The Python and JavaScript variants of the same function return the same result.