import sys
def js_server(module: str, port: int) -> str:
  return '''const net = require('net');
const mymod = require('./{module}');
const serv = net.createServer(function(sock) {ob}    
      sock.on('data', async function(data) {ob}
        const inc = data.toString('utf8');
        const spl = inc.split(';');
        if (spl[0] == '') {ob}
          sock.close();
          return;
        {cb}
        body = JSON.parse(spl.slice(1).join(''));
        const out = await mymod[spl[0]].apply(null, body);
        sock.write(Buffer.from(JSON.stringify(out, 'utf-8'), 'utf-8'));
      {cb});
{cb});
serv.listen({port}, '127.0.0.1');
'''.format(module=module, port=port, empty_obj='{}', ob='{', cb='}')

if __name__ == '__main__':
    print(js_server(sys.argv[1], int(sys.argv[2])))