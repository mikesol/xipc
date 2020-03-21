import logging
from dataclasses import dataclass
from typing import Sequence, Any
import subprocess
import requests
import os
logger = logging.getLogger(__name__)

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
          fi.write(subprocess.check_output(['python', 'py_server.py', script, str(port)]).decode('utf-8'))
          subprocess.Popen(['python', fn])# stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
      elif ('%s.js' % script) in dr:
        fn = '.xipc.%d.js' % port
        with open(fn, 'w') as fi:
          fi.write(subprocess.check_output(['python', 'js_server.py', script, str(port)]).decode('utf-8'))
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
