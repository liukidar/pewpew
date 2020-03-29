import datetime
import network
import json
from lib import cmdutil as cmd
from game import Match, Card, Character
from errorcodes import errorcodes


"""
User class
"""

class User:
  def __init__(self, _username, _websocket):
    self.websocket = _websocket
    self.websocket.username = _username
    self.match = None

  async def send(self, _message, _in_reply_of = None, _code = 501):
    await self.websocket.send(_message, _in_reply_of, _code)

  def name(self):
    return self.websocket.username

"""
GameMng class
"""

class GameMng(network.WsServerHandler):
  def __init__(self):
    super().__init__()
    self.users = {}
    self.matches = {}
    self.decks = {"main": [], "characters": []}
    self.actions = {
      "load_cards": {"f": self.aLoadCards, "p": {}},
      "list_matches": {"f": self.aListMatches, "p": {}},
      "create_match": {"f": self.aCreateMatch, "p": {"matchname": True, "matchpassword": False}},
      "join_match": {"f": self.aJoinMatch, "p": {"matchid": True, "matchpassword": False}},
      "leave_match": {"f": self.aLeaveMatch, "p": {}},
      "start_match": {"f": self.aStartMatch, "p": {"matchid": True}},
    }

    # Loading cards from files
    with open("cards.json", 'r') as file:
      cards = json.loads(file.read())
      for data in cards:
        for card in data["cards"]:
          self.decks["main"].append(Card(card, data))
    with open("characters.json", 'r') as file:
      cards = json.loads(file.read())
      for data in cards:
        self.decks["characters"].append(Character(data))

  ### Actions

  async def aLoadCards(self, _user, _message):
    await _user.send({"cards": [card.__dict__ for deck in self.decks.values() for card in deck]}, _message, 200)

  async def aListMatches(self, _user, _message):
    matches = {}
    for match in self.matches.values():
      matches[match.id] = match.info()

    await _user.send({"matches": matches}, _message, 200)

  async def aCreateMatch(self, _user, _message):
    if _user.match == None:
      m = Match(_message["matchname"], _message["matchpassword"], _user)
      self.matches[m.id] = m
      await _user.send({"match": m.info()}, _message, 200)
    else:
      await _user.send({}, _message, errorcodes["ERR_MATCH_OWNED"])

  async def aJoinMatch(self, _user, _message):
    if _message["matchid"] in self.matches:
      match = self.matches[_message["matchid"]]
      if match.password == _message["matchpassword"]:
        if match.isOpen():
          _user.match = match
          await match.addUser(_user)
          await _user.send({"match": match.info()}, _message, 200)
        else:
          await _user.send({}, _message, errorcodes["ERR_MATCH_NOT_OPEN"])
      else:
        await _user.send({}, _message, errorcodes["ERR_MATCH_PASSWORD_INVALID"])
    else:
      await _user.send({}, _message, errorcodes["ERR_MATCH_NOT_EXIST"])
  
  async def aLeaveMatch(self, _user, _message):
    if _user.match:
      if await _user.match.removeUser(_user) == 0:
        del self.matches[_user.match.id]
      _user.match = None
      await _user.send({}, _message, 200)
    else:
      await _user.send({}, _message, errorcodes["ERR_USER_NOT_IN_MATCH"])

  async def aStartMatch(self, _user, _message):
    if _message["matchid"] in self.matches:
      match = self.matches[_message["matchid"]]
      if _user == match.owner:
        if await match.start(self.decks):
          await _user.send({}, _message, 200)
        else:
          await _user.send({}, _message, errorcodes["ERR_MATCH_NOT_READY"])
      else:
        await _user.send({}, _message, errorcodes["ERR_NOT_MATCH_OWNER"])
    else:
      await _user.send({}, _message, errorcodes["ERR_MATCH_NOT_EXIST"])

  ### Message handling

  async def handle_request(self, _message, _ws):
    if _ws.authorize(_message):
      if _ws.username in self.users:
        user = self.users[_ws.username]
        try:
          # Action processed by the gamemng
          if _message["action"] in self.actions:
            action = self.actions[_message["action"]]
            for param, required in action["p"].items():
              value = _message[param]
              if required and not value:
                raise ValueError(param)
                
            await action["f"](user, _message)
          # Action processed by the target match
          elif "matchid" in _message and _message["matchid"] in self.matches:
            match = self.matches[_message["matchid"]]
            await match.handle_request(user, _message)

        except KeyError as e:
          await user.send({"param": str(e)}, _message, 400)
        except ValueError as e:
          await user.send({"param": str(e)}, _message, 422)
      # Registering
      elif _message["action"] == "register":
        username = _message["username"].lower()
        if username and username not in self.users:
          u = User(username, _ws)
          self.users[u.name()] = u

          await _ws.send({"action": "registered", "username": username}, _message, 200)
        else:
          await _ws.send({}, _message, errorcodes["ERR_TAKEN_USERNAME"])
        
      else:
        await _ws.send({}, _message, 401)
    else:
      await _ws.send({}, _message, 403)

  async def handle_unregister(self, _ws):
    if _ws.username in self.users:
      user = self.users[_ws.username]
      if user.match and await user.match.removeUser(user) == 0:
        del self.matches[user.match.id]
      del self.users[_ws.username]
