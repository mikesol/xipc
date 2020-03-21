import sys

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

if __name__ == '__main__':
    print(py_server(sys.argv[1], int(sys.argv[2])))