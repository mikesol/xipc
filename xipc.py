import logging
from dataclasses import dataclass
from typing import Sequence, Any
import subprocess
import requests
import os
logger = logging.getLogger(__name__)

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

def py_server(module: str, port: int) -> str:
  return '''import tornado.ioloop
import tornado.web
import tornado.escape
import tornado.ioloop
import json
import {module}

class ExecHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ["POST"]
    def post(self, fname):
        body = tornado.escape.json_decode(self.request.body)
        func = getattr({module}, fname)
        res = func(*body)
        self.write(json.dumps(res))
        self.set_header('Content-Type', 'application/json; charset="utf-8"')

class StopHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ["POST"]
    def post(self):
        tornado.ioloop.IOLoop.instance().stop()

def make_app():
    return tornado.web.Application([
        (r"/exec/(.+)", ExecHandler),
        (r"/stop", StopHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen({port})
    tornado.ioloop.IOLoop.current().start()
'''.format(module=module, port=port)

class xipc: pass
def mod(port):
  class _mod:
    def __getattribute__(self, name: str) -> Any:
      def callable(*args):
        url = 'http://localhost:%d/exec/%s' % (port, name)
        return requests.post(url, json=args).json()
      return callable
  return _mod()

class hack:
  my_port = 8000
  start_port = 8001
  end_port = 8001
  def __init__(self, *scripts: str):
    self._scripts = scripts
  def __enter__(self):
    logger.debug("starting xipc")
    port = self.start_port
    out = xipc()
    dr = os.listdir('.')
    for script in self._scripts:
      if ('%s.py' % script) in dr:
        fn = '.xipc.%d.py' % port
        with open(fn, 'w') as fi:
          fi.write(py_server(script, port))
          subprocess.Popen(['python', fn])# stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
      elif ('%s.js' % script) in dr:
        fn = '.xipc.%d.js' % port
        with open(fn, 'w') as fi:
          fi.write(js_server(script, port))
          subprocess.Popen(['node', fn])# stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
      else:
        raise ValueError("Cannot handle %s" % script)
      setattr(out, script, mod(port))
      port += 1
    self.end_port = port
    return out
  def __exit__(self, type, value, traceback):
    for x in range(self.start_port, self.end_port):
      try:
        requests.post('http://localhost:%d/stop' % x)
      except: pass
