from xipc import hack
with hack('py_called_1', 'py_called_2') as mods:
    print(mods.py_called_1.add_ints(1,2))
    print(mods.py_called_2.subtract_ints(1,2))
    print(mods.py_called_1.fortune("Mike"))