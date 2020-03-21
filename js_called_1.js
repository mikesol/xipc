function add_ints(a, b) {
    return a + b;
}

function fortune(name) {
    return { fortune: 'Your name was, is, or will be ' + name + '.'};
}

module.exports = {
    add_ints: add_ints,
    fortune: fortune
};