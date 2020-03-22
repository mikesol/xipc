const { hack } = require("./xipc");
hack("py_called_1")(async (mods) => {
  let res1;
  let res2;
  const py_called_1 = mods.py_called_1;
  let now = new Date().getTime();
  let i = 0;
  for (; i < 1000; i++) {
    await py_called_1("add_ints")(1, 2);
  }
  console.log(
    "Time in seconds for 1000 additions using sockets:",
    (new Date().getTime() - now) / 1000
  );
  now = new Date().getTime();
  i = 0;
  for (; i < 1000; i++) {
    const q = 1 + 2;
  }
  console.log(
    "Time in seconds for 1000 additions:",
    (new Date().getTime() - now) / 1000
  );
});
