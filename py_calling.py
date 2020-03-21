from xipc import hack
with hack(
        'py_called_1',
        'py_called_2',
        'js_called_1',
        'js_called_2'
    ) as mods:
    print("Two values should be the same:",
        mods.py_called_1.add_ints(1,2), # type: ignore
        mods.js_called_1.add_ints(1,2) # type: ignore
    )
    print("Two values should be the same:",
        mods.py_called_2.subtract_ints(1,2), # type: ignore
        mods.js_called_2.subtract_ints(1,2), # type: ignore
    )
    print("Two values should be the same:",
        mods.py_called_1.fortune("Mike"), # type: ignore
        mods.js_called_1.fortune("Mike"), # type: ignore
    )