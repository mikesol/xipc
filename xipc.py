import logging
from dataclasses import dataclass
from typing import Sequence, Any
import subprocess
import requests
logger = logging.getLogger(__name__)

def server(module: str, port: int) -> str:
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
    for script in self._scripts:
      fn = '.xipc.%d.py' % port
      with open(fn, 'w') as fi:
        fi.write(server(script, port))
        subprocess.Popen(['python', fn], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        setattr(out, script, mod(port))
        port += 1
    self.end_port = port
    return out
  def __exit__(self, type, value, traceback):
    for x in range(self.start_port, self.end_port):
      try:
        requests.post('http://localhost:%d/stop' % x)
      except: pass
