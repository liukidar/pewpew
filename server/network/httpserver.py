import http.server
import json
import os
import pyperclip
import threading
import datetime
import random
import asyncio

class HttpServerHandler(http.server.BaseHTTPRequestHandler):
  def handle_request(self, _post_data):
    return ({"ip": self.server.server_address[0], "port": self.server.server_address[1]}, 200)

  def _http_output(self, _bin_stream, _code = 200, _headers = {}):
    self.send_response(_code)
    for header, value in _headers.items():
      self.send_header(header, value)

    output = None
    if type(_bin_stream) == str:
      output = _bin_stream.encode("utf-8")
    elif type(_bin_stream) == dict:
      output = json.dumps(_bin_stream).encode("utf-8")
    else:
      output = _bin_stream

    self.end_headers()
    self.wfile.write(output)

  def log_message(self, format, *args):
    return

  def do_GET(self):
    try:
      with open("dist" + self.path, "rb") as page:
        if os.path.dirname(os.path.realpath(page.name)).find(os.path.dirname(os.path.realpath(__file__)) + "\\dist") == 0:
          self._http_output(page.read())
        else:
          self._http_output("Access denied", 401)
    except IOError:
      self._http_output("File {} not found".format(self.path), 404)     

  def do_POST(self):
    if self.path == '/api':
      if (self.headers["Content-Type"] == "application/json"):
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length))

        (response_data, code) = self.handle_request(post_data)

        self._http_output(response_data, code)
      else:
        self._http_output("Content-Type: {} not supported".format(self.headers["Content-Type"]))

  def do_OPTIONS(self):
        self.send_response(200)
        # self.send_header("Access-Control-Allow-Origin", self.headers["origin"])
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

class HttpServer:

  ### private
  __status_msgs = {
    "creating": "[{}] http://{}:{} - Creating http server.",
    "created": "[{}] http://{}:{} - Http server created successfully!",
    "running": "[{}] http://{}:{} - Listening for http requests.",
    "stopped": "[{}] http://{}:{} - Http server stopped successfully."
  }

  def __start(self, _semaphore):
    self.set_status("creating")
    self.loop = asyncio.new_event_loop()
    pyperclip.copy(self.address[0] + "/index.html")
    self.server = http.server.HTTPServer(self.address, self.handler)
    self.set_status("created")
    self.loop.run_until_complete(self.__run(_semaphore))
    
  async def __run(self, _semaphore):
    self.set_status("running")
    if _semaphore:
      _semaphore.release()
    self.server.serve_forever()

  ### public
  def __init__(self, _handler = HttpServerHandler):
    self.handler = _handler

  def run(self, _address, _semaphore = None):
    self.address = _address
    self.th = threading.Thread(target=self.__start, args=(_semaphore,))
    self.th.start()

  def shutdown(self):
    self.server.shutdown()
    self.th.join()
    self.set_status("stopped")

  def set_status(self, _new_status):
    print(self.__status_msgs[_new_status].format(datetime.datetime.now().time(), self.address[0], self.address[1]))
    self.status = _new_status


