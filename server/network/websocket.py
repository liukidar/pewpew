import asyncio
import websockets
import random
import threading
import datetime
import uuid
import json

class WsUser:
  def __init__(self, _websocket, _auth):
    self.websocket = _websocket
    self.username = None
    self.auth = _auth
    self.msgs = []
    self.ready = asyncio.Event()

  def __repr__(self):
    return self.ip()

  def ip(self):
    return self.websocket.remote_address[0] + ":" + str(self.websocket.remote_address[1])

  async def send(self, _message, _in_replay_of = None, _status = 501):
    if _in_replay_of:
      _message['requestId'] = _in_replay_of['requestId']
      _message['status'] = _status
    self.msgs.append(json.dumps(_message))
    self.ready.set()

  async def pop(self):
    await self.ready.wait()
    self.ready.clear()
    msgs = self.msgs
    self.msgs = []

    return msgs

  def authorize(self, _message):
    if ("auth" in _message):
      return self.auth == _message["auth"]
    else:
      return False

class WsServerHandler:
  def __init__(self):
    self.__users = {}
    self.loop = None

  async def handle_request(self, _message, _user):
    pass

  async def handle_unregister(self, _user):
    pass

  async def send_to_ips(self, _msg, _ips):
    for ip in _ips:
      await self.__users[ip].send(_msg)

  async def send_to_all(self, _msg, _except=set()):
    for user in self.__users.values():
      if user not in _except:
        await user.send(_msg)

  async def __register(self, _websocket):
    user = WsUser(_websocket, str(uuid.uuid4()))
    self.__users[_websocket.remote_address] = user
    await _websocket.send(json.dumps({"auth": user.auth, "ip": user.ip()}))
  
  async def __unregister(self, _websocket):
    del self.__users[_websocket.remote_address]

  async def __handle_request(self, websocket):
    async for message in websocket:
      await self.handle_request(json.loads(message), self.__users[websocket.remote_address])

  async def __produce_request(self, websocket):
    while True:
      for msg in await self.__users[websocket.remote_address].pop():
        await websocket.send(msg)

  async def request(self, _websocket, _path):
    await self.__register(_websocket)
    try:
      consumer_task = asyncio.create_task(
        self.__handle_request(_websocket))
      producer_task = asyncio.create_task(
        self.__produce_request(_websocket))
      (_, pending) = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
      )
      for task in pending:
          task.cancel()
    finally:
      await self.handle_unregister(self.__users[_websocket.remote_address])
      await self.__unregister(_websocket)

class WsServer:

  ### private
  statusMsgs = {
    "creating": "[{}] ws://{}:{} - Creating websocket service.",
    "created": "[{}] ws://{}:{} - Websocket server created successfully!",
    "running": "[{}] ws://{}:{} - Listening for websocket requests.",
    "stopped": "[{}] ws://{}:{} - Websocket service stopped successfully."
  }

  async def __run(self, _semaphore):
    async with websockets.serve(self.handler.request, self.address[0], self.address[1]):
      self.set_status("running")
      if _semaphore:
        _semaphore.release()
      await self.stop_condition

  def __start(self, _semaphore):
    self.set_status("creating")
    self.handler.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self.handler.loop)
    self.stop_condition = self.handler.loop.create_future()
    self.set_status("created")
    self.handler.loop.run_until_complete(self.__run(_semaphore))
    
  ### public
  def __init__(self, _handler = WsServerHandler()):
    self.handler = _handler

  def run(self, _address, _semaphore = None):
    self.address = _address
    self.th = threading.Thread(target=self.__start, args=(_semaphore,))
    self.th.start()
    
  def shutdown(self):
    self.handler.loop.call_soon_threadsafe(self.stop_condition.set_result, None)
    self.th.join()
    self.set_status("stopped")
  
  def set_status(self, _new_status):
    print(self.statusMsgs[_new_status].format(datetime.datetime.now().time(), self.address[0], self.address[1]))
    self.status = _new_status
