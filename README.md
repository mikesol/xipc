# xipc

Hackish experiment in interprocess communication.  It allows Python to "call" JavaScript functions.

## Install

Create a Python virtualenv and activate it. Then:

```bash
npm install
```

## Run Python

Check out [`py_calling.py`](./py_calling.py). It uses a library called [`xipc`](./xipc.py), which is in this repo. The top-level `with` statement "imports" four modules:

- [`py_called_1`](./py_called_1.py)
- [`py_called_2`](./py_called_2.py)
- [`js_called_1`](./js_called_1.js)
- [`js_called_2`](./js_called_2.js)

Then, it calls functions in these modules. The Python and JavaScript variants of each function return the same results, which you can see from the CLI output.

```bash
$ python py_calling.py
Two values should be the same: 3 3
Two values should be the same: -1 -1
Two values should be the same: {'fortune': 'Your name was, is, or will be Mike.'} {'fortune': 'Your name was, is, or will be Mike.'}
```

## Run JavaScript

Check out [`js_calling.js`](./js_calling.js). It uses a library called [`xipc`](./xipc.js), which is in this repo. The top-level function "imports" four modules:

- [`py_called_1`](./py_called_1.py)
- [`py_called_2`](./py_called_2.py)
- [`js_called_1`](./js_called_1.js)
- [`js_called_2`](./js_called_2.js)

Then, it calls functions in these modules. The Python and JavaScript variants of each function return the same results, which you can see from the CLI output.

```
$ node js_calling.js
Two values should be the same: 3 3
Two values should be the same: -1 -1
Two values should be the same: { fortune: 'Your name was, is, or will be Mike.' } { fortune: 'Your name was, is, or will be Mike.' }
```

## Profiling

Run:

```bash
$ python prof.py
Time in seconds for 1000 additions using sockets: 0.17347383499145508
Time in seconds for 1000 additions: 0.0
$ node prof.js
Time in seconds for 1000 additions using sockets: 0.681
Time in seconds for 1000 additions: 0
```