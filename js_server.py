import sys
def js_server(module: str, port: int) -> str:
  return '''const express = require('express');
  const bodyParser = require('body-parser');
  const mymod = require('./{module}');
  const app = express();
  let _ = {empty_obj};
  app.post("/exec/:fname", bodyParser.json(), async (req, res) => {ob}
    const out = await mymod[req.params.fname].apply(null, req.body);
    res.json(out);
  {cb});
  app.post("/stop", (_, res) => {ob}
    res.send("");
    process.exit();
  {cb});
  _.server = app.listen({port}, () => {empty_obj});
'''.format(module=module, port=port, empty_obj='{}', ob='{', cb='}')

if __name__ == '__main__':
    print(js_server(sys.argv[1], int(sys.argv[2])))