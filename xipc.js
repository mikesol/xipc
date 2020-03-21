const fs = require('fs');
const net = require('net');
const child_process = require('child_process');

const xipc = () => ({});
const mod = port => {
  return new Promise((resolve, reject) => {
    const client = new net.Socket();
    client.connect(port, () => {
      console.log("RESOLVING");
      resolve(new Proxy({}, {
        get: function(target, name, receiver) {
          console.log("returning fn", name);
          return function() {
            console.log("CALLED");
            const argz = new Array(arguments.length).fill(null);
            let i = 0;
            for (; i < argz.length; i++) {
              argz[i] = arguments[i];
            }
            const toWrite = name + ';' + JSON.stringify(argz, 'utf-8');
            return new Promise((res, rej) => {
              client.on('data', (d) => {
                console.log("DATA", d);
                res(JSON.parse(d.toString('utf-8')));
              });
              console.log("IN PROM", toWrite);
              client.write(Buffer.from(toWrite, 'utf-8'));
            });  
          };
        },
        set: function(target, name, value, receiver) {
          throw Exception('Cannot set mod.')
        }
      }));
    });
  });
};

const hack = function () {
  const scripts = arguments;
  return async function (f) {
    const start_port = 8001;
    let end_port = 8001;
    let port = start_port;
    const out = xipc();
    const dr = fs.readdirSync('.');
    let i = 0;
    console.log("starting loop");
    for(; i < scripts.length; i++) {
      const script = scripts[i];
      if (dr.indexOf(script+'.py') !== -1) {
        const fn = '.xipc.'+port+'.py';
        fs.writeFileSync(fn, child_process.execSync('python py_server.py ' + script + ' ' + port));
        child_process.spawn("python", [fn], { detached: true, stdio: "ignore", windowsHide: true });
      } else if (dr.indexOf(script+'.js') !== -1) {
        const fn = '.xipc.'+port+'.js';
        fs.writeFileSync(fn, child_process.execSync('python js_server.py ' + script + ' ' + port));
        child_process.spawn("node", [fn], { detached: true, stdio: "ignore", windowsHide: true });
      } else {
        throw Exception("Cannot handle " + script)
      }
      console.log("awaiting mod");
      out[script] = await mod(port);
      console.log("O", script, out[script]);
      port += 1
    }
    end_port = port
    try {
      await f(out)
    } catch (e) {
      console.log(e);
    }
    i = start_port;
    for (; i < end_port; i++) {
      const client = new net.Socket();
      client.connect(i, () => {
        client.write(';');
      });
    }
  };
}

module.exports = { hack: hack };