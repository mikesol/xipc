const { hack } = require('./xipc');
hack(
    'py_called_1',
    'py_called_2',
    'js_called_1',
    'js_called_2'
)(async mods => {
    let res1;
    let res2;
    console.log('pc0');
    const py_called_1 = await mods.py_called_1;
    console.log('pc1', py_called_1);
    const py_called_2 = await mods.py_called_2;
    const js_called_1 = await mods.js_called_1;
    const js_called_2 = await mods.js_called_2;
    res1 = await py_called_1.add_ints(1,2);
    res2 = await js_called_1.add_ints(1,2);
    console.log("Two values should be the same:", res1, res2);
    res1 = await py_called_2.subtract_ints(1,2);
    res2 = await js_called_2.subtract_ints(1,2);
    console.log("Two values should be the same:", res1, res2);
    res1 = await py_called_1.fortune("Mike"),
    res2 = await js_called_1.fortune("Mike"),
    console.log("Two values should be the same:", res1, res2);
});