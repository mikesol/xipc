const xipc = require('./xipc');

xipc(
    'py_called_1',
    'py_called_2',
    'js_called_1',
    'js_called_2'
)(mods => {
    console.log("Two values should be the same:",
        mods.py_called_1.add_ints(1,2),
        mods.js_called_1.add_ints(1,2)
    );
    console.log("Two values should be the same:",
        mods.py_called_2.subtract_ints(1,2),
        mods.js_called_2.subtract_ints(1,2),
    );
    console.log("Two values should be the same:",
        mods.py_called_1.fortune("Mike"),
        mods.js_called_1.fortune("Mike"),
    );
});