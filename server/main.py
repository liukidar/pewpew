import datetime
import random
import network
import gamemng
import lib.cmdutil as cmd
import lib.webutil as webutil

if __name__ == "__main__":
  random.seed() 
  cmd.clear()
  print("\n\n### e2dSimpleServer.py ###\n\n")
  port = 8080

  g = gamemng.GameMng()
  
  adapter = webutil.select_adapter()
  cmd.clear()
  print("Adapter: " + adapter.nice_name, "Ip: " + adapter.ipv4, sep='\n', end='\n\n')

  ns = webutil.NetworkService((adapter.ipv4, port), [
    network.HttpServer(),
    network.WsServer(g)
  ])

  ns.run()

  try:
    while True:
      i = input("\n> ")
      if len(i):
        try:
          r = eval(i)
          if r is not None:
            print("[{}] - {}".format(datetime.datetime.now().time(), r))
        except Exception as e:
          print(type(e).__name__, e)
  except KeyboardInterrupt:
    print("KeyboardInterrupt\n")

  ns.shutdown()
