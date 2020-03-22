const fs = require("fs");
const net = require("net");
const child_process = require("child_process");

const xipc = () => ({});
const makeClient = (port) => {
  return new Promise((resolve, reject) => {
    const client = new net.Socket();
    client.connect(port, () => {
      resolve(client);
    });
  });
};
const mod = (client) => {
  return new Proxy(
    {},
    {
      get: function (_, name) {
        return function () {
          const argz = new Array(arguments.length).fill(null);
          let i = 0;
          for (; i < argz.length; i++) {
            argz[i] = arguments[i];
          }
          const toWrite = name + ";" + JSON.stringify(argz, "utf-8");
          return new Promise((res, rej) => {
            let l = (d) => {
              res(JSON.parse(d.toString("utf-8")));
              client.removeListener("data", l);
            };
            client.on("data", l);
            client.write(Buffer.from(toWrite, "utf-8"));
          });
        };
      },
      set: function () {},
    }
  );
};

const hack = function () {
  const scripts = arguments;
  return async function (f) {
    const start_port = 8001;
    let end_port = 8001;
    let port = start_port;
    const out = xipc();
    const dr = fs.readdirSync(".");
    let i = 0;
    for (; i < scripts.length; i++) {
      const script = scripts[i];
      if (dr.indexOf(script + ".py") !== -1) {
        const fn = ".xipc." + port + ".py";
        fs.writeFileSync(
          fn,
          child_process.execSync("python py_server.py " + script + " " + port)
        );
        child_process.spawn("python", [fn], {
          detached: true,
          stdio: "ignore",
          windowsHide: true,
        });
      } else if (dr.indexOf(script + ".js") !== -1) {
        const fn = ".xipc." + port + ".js";
        fs.writeFileSync(
          fn,
          child_process.execSync("python js_server.py " + script + " " + port)
        );
        child_process.spawn("node", [fn], {
          detached: true,
          stdio: "ignore",
          windowsHide: true,
        });
      } else {
        throw Exception("Cannot handle " + script);
      }
      const client = await makeClient(port);
      out[script] = mod(client);
      port += 1;
    }
    end_port = port;
    try {
      await f(out);
    } catch (e) {
      console.log(e);
    }
    i = start_port;
    for (; i < end_port; i++) {
      const client = new net.Socket();
      client.connect(i, () => {
        client.write(";");
        client.destroy();
      });
    }
    process.exit(0);
  };
};

module.exports = { hack: hack };
