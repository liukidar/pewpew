from game import Match
from gamemng import User
import uuid

"""
execute_action() {
  <= action: 'play_card', type: 'damage', damage:1, to:'pippo', from:'luca', range: 1, required_miss = 1, is_bang: true, queue = {}
  from player:
    (outgoing) -  #1: weapon (range) => 4
                  #2: character required_miss = 2
                  #3: weapon_2 (is_bang) => false
                  #4: sniper (queue: reveal) = if diamonds => required miss = inf
    - temp_effect = apply_queue (=>) # execute_action(for el in queue)
  to each target:
    (incoming)  - #1: horse (range) => range - 1
                  #2: barrel (queue: reveal) = if heart => required_miss - 1 else nothing
    - result_effect = apply_queue (=>)
    => apply_effect
}
"""

class Script:
  requests = {
    "id": {e: _Eff}, "id2":{}
  }

  def resolve(self, _effect, _res, _message):
    if _res in _effect['modifiers']:
      e = _effect['modifiers'][_res]
      e_property = e['property']
      e_magnitude = e['magnitude']
      e_operation = e['operation']

      if e_operation is 'add':
        _message[e_property] += e_magnitude
      elif e_operation is 'set':
        _message[e_property] = e_magnitude
      else:
        print('You should never arrive here. If you do, you\'re lost.')
    else:
      print('No effect can be triggered based on the conditions.')
    
  def execute(self, _match: Match, _user: User, _message: {}):
    player = _match.players[_user.name()]

    for card in player.board:
      for (name, effects) in card.effects['incoming'].items():
        if name in _message:
          for effect in effects:
            res = self.fork_conditions(effect['conditions']) # ==> execute
            if res is None:
              resolve(effect, )
            # else resolve immediately
            
            #send message of action
          

  def fork_conditions(self, _conditions: {}):
    if not _conditions:
      return 'any'
    
    message = {}
    message['action'] = _conditions['action']
    for (optionName, option) in _conditions['options'].items():
      message[optionName] = option

    # execute

    #sleep until rispsota

    return 'pass'


