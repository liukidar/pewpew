import uuid
import random
import collections
import json
import copy

class Card:
  
  def __init__(self, _card, _dict):
    self.suit = _card["suit"]
    self.value = _card["value"]
    self.type = _dict["type"]
    self.name = _dict["name"]
    self.text = _dict["text"]
    self.image = _dict["image"]
    self.hid = 'pv_' + '{:x}'.format(abs(hash(str(self.suit)) + hash(str(self.value)) + hash(str(self.name)) + hash(str(self.type))))
    
  def setPid(self, _i):
    self.pid = 'pb_' + '{:x}'.format(_i)

  def __hash__(self):
    return self.hid

class EffectCard:
  def __init__(self):
    self.incoming = {'bang': {'action': 'add', 'effect': 'reveal'}}
    self.outgoing = {}

class Character(Card):
  def __init__(self, _dict):
    super().__init__({"suit": None, "value": None}, _dict)
    self.life = _dict["life"]

class CardList:
  def __init__(self):
    self.cards = collections.deque()

  def getPublic(self):
    return [{"pid": card.pid} for card in self.cards]
  def getPrivate(self):
    return [{"pid": card.pid, "hid": card.hid} for card in self.cards]

  def _add(self, _card_s):
    if type(_card_s) == CardList:
      self.cards.extend(_card_s.cards)
    elif isinstance(_card_s, list):
      self.cards.extend(_card_s)
    else:
      self.cards.append(_card_s)
  def _remove(self, _card_hid):
    for card in self.cards:
      if card.hid == _card_hid:
        self.cards.remove(card)

        return card
      
    return None

  def get(self, _hid):
    for el in self.cards:
      if el.hid == _hid:
        return el

    return None

  # V 0.1
  def _remove_by_pid(self, _card_pid):
    for card in self.cards:
      if card.pid == _card_pid:
        self.cards.remove(card)

        return card
      
    return None

class Deck(CardList):
  def __init__(self, _cards):
    super().__init__()
  
    for card in _cards:
      self._add(copy.deepcopy(card))
    self.shuffle()
    
    for i, card in enumerate(self.cards):
      card.setPid(i)

  def shuffle(self):
    random.shuffle(self.cards)

  def draw(self, _amount):
    l = CardList()
    for i in range(_amount):
      l._add(self.cards.popleft())

    return l

  def isEmpty(self):
    return len(self.cards) == 0

class Hand(CardList):
  def draw(self, _deck, _amount):
    r = _deck.draw(_amount)
    self._add(r)

    return r

  def play(self, _card_hid):
    return self._remove(_card_hid)

class Board(CardList):
  pass

class Player:
  def __init__(self, _user, _role):
    self.user = _user
    self.role = _role
    self.hand = Hand()
    self.board = Board()
    self.character = None
    self.life = 0
    self.maxlife = 0

  def setCharacter(self, _card):
    self.character = _card.hid
    self.maxlife = _card.life + (1 if self.role == 'sheriff' else 0)
    self.life = self.maxlife

  def info(self):
    return {"name": self.user.name(), "character": {"hid": self.character}, "life": self.life, "maxlife": self.maxlife}

class Match:
  MIN_PLAYERS = 1
  MAX_PLAYERS = 9
  ROLES = {
    1: ['sheriff'],
    2: ['sheriff', 'renegade'],
    3: ['bandit', 'sheriff', 'renegade'],
    4: ['bandit', 'bandit', 'sheriff', 'renegade'],
    5: ['bandit', 'bandit', 'sheriff', 'deputy', 'renegade'],
    6: ['bandit', 'bandit', 'bandit', 'sheriff', 'deputy', 'renegade'],
    7: ['bandit', 'bandit', 'bandit', 'sheriff', 'deputy', 'deputy', 'renegade'],
    8: ['bandit', 'bandit', 'bandit', 'sheriff', 'deputy', 'deputy', 'renegade', 'renegade'],
    9: ['bandit', 'bandit', 'bandit', 'bandit', 'sheriff', 'deputy', 'deputy', 'renegade', 'renegade']
  }

  def __init__(self, _name, _password, _owner):
    # Match metadata
    self.id = str(uuid.uuid4())
    self.name = _name
    self.password = _password
    self.cardlist = None # TODO
    self.owner = _owner
    self.users = [_owner]
    self.status = 'open'
    _owner.match = self

    self.actions = {
      "p_select_character": {"f": self.aPlayerSetCharacter, "p": {"pid": True}},
      "p_get_start_data": {"f": self.aGetMatchStartData, "p": {}},
      #"p_draw": {"f": self.aPlayerDraw, "p": {"amount": True}},
      #"p_play": {"f": self.aPlayerPlay, "p": {"hid": True}},
      #"p_reveal": {"f": self.aPlayerReveal, "p": {"amount": True}},
      #"p_pick_revealed": {"f": self.aPlayerPickRevealed, "p": {"hid": True}},
      "p_move_card": {"f": self.aCardMove, "p": {}},
      "p_shuffle": {"f": self.aShuffle, "p": {}},
      "p_set_life": {"f": self.aSetLife, "p": {}},
      "p_pass_turn": {"f": self.aPassTurn, "p": {}}
    }

    # Match data
    self.readyPlayers = 0
    self.players = {}
    self.turns = []
    self.turn = 0
    self.activePlayers = []
    self.decks = {}
    self.currentTurn = None # [0...len(self.players)]

    # V 0.1
    self.revealed = CardList()
    self.discards = CardList()

  def isPlayerActive(self, _user):
    return 1 or (_user.name() in self.activePlayers) or (len(self.activePlayers) == 0 and self.turn == _user.name())

  #######################
  
  async def __broadcast(self, _message, _exception=None):
    if isinstance(_exception, list):
      to = filter(lambda p: p not in _exception, self.users)
    else:
      to = filter(lambda p: p != _exception, self.users)

    for u in to:
      await u.send(_message)

  async def start(self, _decks):
    if len(self.users) > self.MIN_PLAYERS - 1 and self.status == 'open':
      # setting status
      self.status = 'ready'

      # create _decks
      self.decks["main"] = Deck(_decks["main"])
      self.decks["characters"] = Deck(_decks["characters"])

      # creating players with roles
      roles = [role for role in self.ROLES[len(self.users)]]
      for player in self.users:
        role = random.choice(roles)
        self.players[player.name()] = Player(player, role)
        roles.remove(role)

      # assigning characters
      characters = self.decks["characters"].draw(len(self.users))
      for player, character in zip(self.players.values(), characters.cards):
        player.setCharacter(character)

      # create turns
      self.turns = list(self.players.keys())
      random.shuffle(self.turns)
      self.turn = iter(self.turns)
      self.turnPlayer = self.players[next(self.turn)]
      while self.turnPlayer.role != 'sheriff':
        self.turnPlayer = self.players[next(self.turn)]

      await self.__broadcast({"event": "match_edit", "match": self.info()})

      return True
    else:
      return False

  async def addUser(self, _user):
    self.users.append(_user)
    for user in self.users:
      await user.send({"event": "match_edit", "match": self.info()})

  async def removeUser(self, _user):
    if _user in self.users:
      self.users.remove(_user)
      if self.owner == _user and len(self.users):
        self.owner = self.users[0]
      for user in self.users:
        await user.send({"event": "match_edit", "match": self.info()})
    return len(self.users)

  def info(self):
    return {"id": self.id, "name": self.name, "owner": self.owner.name(), "players": list(map(lambda p: p.name(), self.users)), "status": self.status}

  ###################
  #####
  ##### ACTIONS #####
  #####
  ###################
  
  ################################################################
  ##### V 0.1
  ################################################################

  async def aGetMatchStartData(self, _user, _message):
    await _user.send({"turns": self.turns, "sheriff": self.turnPlayer.user.name(), "role": self.players[_user.name()].role, "players": [player.info() for player in self.players.values()]}, _message, 200)

  async def aCardMove(self, _user, _message):
    owner = _message["from"].split('/')
    if owner[0] == 'deck':
      if self.decks["main"].isEmpty():
        await _user.send({}, _message, 818)

        return
      else:
        card = self.decks["main"].draw(1).cards[0]
    elif owner[0] == 'discards':
      card = self.discards._remove(_message["hid"])
    elif owner[0] == 'revealed':
      card = self.revealed._remove(_message["hid"])
    elif owner[0] == 'hand':
      if "hid" in _message:
        card = self.players[owner[1]].hand._remove(_message["hid"])
      else:
        card = self.players[owner[1]].hand._remove_by_pid(_message["pid"])
    elif owner[0] == 'board':
      card = self.players[owner[1]].board._remove(_message["hid"])
      
    target = _message["to"].split('/')
    if target[0] == 'deck':
      self.decks["main"]._add(card)
  
      await self.__broadcast({"event": "card_moved", "to": _message["to"], "from": _message["from"],  "card": {"pid": card.pid}}, _user)
      await _user.send({"to": _message["to"], "from": _message["from"], "card": {"pid": card.pid, "hid": card.hid}}, _message, 200)

    elif target[0] == 'discards':
      self.discards._add(card)

      await self.__broadcast({"event": "card_moved", "to": _message["to"], "from": _message["from"],  "card": {"pid": card.pid, "hid": card.hid}}, _user)
      await _user.send({"to": _message["to"], "from": _message["from"], "card": {"pid": card.pid, "hid": card.hid}}, _message, 200)
    elif target[0] == 'revealed':
      self.revealed._add(card)

      await self.__broadcast({"event": "card_moved", "to": _message["to"], "from": _message["from"],  "card": {"pid": card.pid, "hid": card.hid}}, _user)
      await _user.send({"to": _message["to"], "from": _message["from"], "card": {"pid": card.pid, "hid": card.hid}}, _message, 200)
    elif target[0] == 'hand':
      self.players[target[1]].hand._add(card)
      
      await self.__broadcast({"event": "card_moved", "to": _message["to"], "from": _message["from"],  "card": {"pid": card.pid}}, [_user, self.players[target[1]].user])
      if _user != self.players[target[1]].user:
        await self.players[target[1]].user.send({"event": "card_moved", "to": _message["to"], "from": _message["from"],  "card": {"pid": card.pid, "hid": card.hid}})
      await _user.send({"to": _message["to"], "from": _message["from"], "card": {"pid": card.pid, "hid": card.hid}}, _message, 200)
    elif target[0] == 'board':
      self.players[target[1]].board._add(card)

      await self.__broadcast({"event": "card_moved", "to": _message["to"], "from": _message["from"],  "card": {"pid": card.pid, "hid": card.hid, "bottom": _message["card-bottom"], "left": _message["card-left"]}}, _user)
      await _user.send({"to": _message["to"], "from": _message["from"], "card": {"pid": card.pid, "hid": card.hid, "bottom": _message["card-bottom"], "left": _message["card-left"]}}, _message, 200)
      
  async def aShuffle(self, _user, _message):
    self.decks["main"]._add(self.discards)
    self.discards = CardList()

    await self.__broadcast({"event": "deck_shuffled"}, _user)
    await _user.send({}, _message, 200)

  async def aSetLife(self, _user, _message):
    player = self.players[_user.name()]
    player.life = _message["life"]

    if player.life == 0:
      await self.__broadcast({"event": "reveal_role", "player": player.user.name(), "role": player.role}, _user)


    await self.__broadcast({"event": "set_life", "player": player.info()}, _user)
    await _user.send({"player": player.info()}, _message, 200)

  async def aPassTurn(self, _user, _message):
    try:
      while True:
        self.turnPlayer = self.players[next(self.turn)]
        if self.turnPlayer.life != 0:
          break
    except StopIteration:
      self.turn = iter(self.turns)
      while True:
        self.turnPlayer = self.players[next(self.turn)]
        if self.turnPlayer.life != 0:
          break

    await self.__broadcast({"event": "set_turn", "turn": self.turnPlayer.user.name()}, _user)
    await _user.send({"turn": self.turnPlayer.user.name()}, _message, 200)

  #### END - V 0.1

  async def aPlayerDraw(self, _user, _message):
    if self.isPlayerActive(_user):
      player = self.players[_user.name()]
      cards = player.hand.draw(self.decks["characters"], _message["amount"])

      await self.__broadcast({"event": "edit_hand", "player": _user.name(), "new_cards": cards.getPublic()}, _user)
      await _user.send({"player": _user.name(), "new_cards": cards.getPrivate()}, _message, 200)

  async def aPlayerReveal(self, _user, _message):
    if self.isPlayerActive(_user):
      self.revealed._add(self.decks["characters"].draw(_message["amount"]))

      await self.__broadcast({"event": "cards_revealed", "cards": self.revealed.getPrivate()}, _user)
      await _user.send({"cards": self.revealed.getPrivate()}, _message, 200)

  async def aPlayerPickRevealed(self, _user, _message):
    if self.isPlayerActive(_user):
      card = self.revealed._remove(_message["hid"])
      self.players[_user.name()].hand._add(card)

      await self.__broadcast({"event": "card_picked", "player": _user.name(), "pid": card.pid}, _user)
      await _user.send({"player": _user.name(), "pid": card.pid}, _message, 200)

  async def aPlayerPlay(self, _user, _message):
    if self.isPlayerActive(_user):
      player = self.players[_user.name()]
      card = player.hand.play(_message["hid"])



     # await self.__broadcast({"event": "card_played", "from": _user.name(), "pid": card.pid, "hid": card.hid, "to": target}, _user)
      #await _user.send({"from": _user.name(), "pid": card.pid, "hid": card.hid, "to": _user.name()}, _message, 200)

      # _message["to"] = array of targets

  async def aPlayerSetCharacter(self, _user, _message):
    self.players[_user.name()].selectCharacter(_message['pid'])
    self.readyPlayers += 1
    
    await _user.send({}, _message, 200)

    if self.readyPlayers == len(self.players):
      await self.__broadcast({"event": "match_started", "characters": map(lambda p: p.character.hid, self.players)})
      # begin turn of first player


  # user.name() da la chiave di self.players
  async def handle_request(self, _user, _message):
    if _message["action"] in self.actions:
      action = self.actions[_message["action"]]
      for param, required in action["p"].items():
        value = _message[param]
        if required and not value:
          raise ValueError(param)
          
      await action["f"](_user, _message)

  def isOpen(self):
    return self.status == 'open' and len(self.users) < self.MAX_PLAYERS

  def isOver(self):
    pass # if sheriff == dead or renegade, outlaw == dead, dead


  
