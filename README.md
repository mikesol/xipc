# xipc

Hackish experiment in interprocess communication.  It allows Python to "call" JavaScript functions.

## Install

Create a Python virtualenv and activate it. Then:

```bash
npm install
pip install -r requirements.txt
```

## Run

Check out [`py_calling.py`](./py_calling.py). It uses a library called [`xipc`](./xipc.py), which is in this repo. The top-level `with` statement "imports" four modules:

- [`py_called_1.py`](./py_called_1.py)
- [`py_called_2.py`](./py_called_2.py)
- [`js_called_1.js`](./js_called_1.js)
- [`js_called_2.js`](./js_called_2.js)

Then, it calls a bunch of functions in these modules. The Python and JavaScript variants of each function return the same results, which you can see from the CLI output.