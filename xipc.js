const fs = require('fs');
const child_process = require('child_process');
const axios = require('axios');

const xipc = () => ({});
const mod = port => {
  return new Proxy({}, {
    get: function(target, name, receiver) {
      return async function() {
        const url = 'http://localhost:'+port+'/exec/'+name;
        const argz = new Array(arguments.length).fill(null);
        let i = 0;
        for (; i < argz.length; i++) {
          argz[i] = arguments[i];
        }
        const { data } = await axios.post(url, argz);
        return data;
      };
    },
    set: function(target, name, value, receiver) {
      throw Exception('Cannot set mod.')
    }
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
      out[script] = mod(port);
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
      try {
        axios.post('http://localhost:'+i+'/stop');
      } catch {}
    }
  };
}

module.exports = { hack: hack };