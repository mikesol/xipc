const fs = require('fs');
const child_process = require('child_process');

const xipc = () => ({});
const mod = port => {
  return new Proxy({}, {
    get: async function(target, name, receiver) {
      return function() {
        const url = 'http://localhost:'+port+'/exec/'+name % (port, name)
        const { data } = await axios.post(url, arguments);
        return data;
      };
    },
    set: function(target, name, value, receiver) {
      throw Exception('Cannot set mod.')
    }
  });
};

const hack = async function () {
  const scripts = arguments;
  return async function (f) {
    const start_port = 8001;
    let end_port = 8001;
    let port = start_port;
    const out = xipc();
    const dr = fs.readdirSync('.');
    let i = 0;
    for(; i < scripts; i++) {
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
    } catch {}
    var i = start_port;
    for (; i < end_port; i++) {
      try {
        axios.post('http://localhost:'+i+'/stop');
      } catch {}
    }
  };
}

module.exports = hack;