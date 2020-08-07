import ifaddr
import msvcrt
import threading

class NetworkService:
  def __init__(self, _address, _services):
    self._address = _address
    self.services = _services

  def run(self):
    semaphore = threading.Semaphore(0)
    for i, service in enumerate(self.services):
      service.run((self._address[0], self._address[1] + i), semaphore)

    for _ in self.services:
      semaphore.acquire()

  def shutdown(self):
    for s in self.services:
      s.shutdown()

def list_adapters(_output=True):
  if _output:
    print("List of networks interfaces:\n")

  adapters = ifaddr.get_adapters()
  for i, adapter in enumerate(adapters):
    if _output:
      print(str(i) + ": " + adapter.nice_name)
    for ip in adapter.ips:
      if ip.is_IPv4:
        adapter.ipv4 = ip.ip
        if _output:
          print("   %s/%s" % (ip.ip, ip.network_prefix))

  return adapters

def select_adapter():
  adapters = list_adapters()
  
  print("\nWhich adapter to use?")
  interface = -1
  while True:
    if interface == -1:
      print("~ Localhost: 127.0.0.1", end="\r")
    else:
      print((str(interface) + ": " + adapters[interface].nice_name).ljust(64), end="\r")
    c = msvcrt.getch()
    if ord(c) == 13:
      break
    elif ord("0") <= ord(c) < ord("0") + len(adapters):
      interface = int(c)

  return adapters[interface]
