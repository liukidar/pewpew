import Vue from 'vue'
import { APIRequest, APIAddEventListener } from '../api'
import { pushError } from '../msgmanager'

function player(_name) {
  let name = _name
  let role = 'unknown'
  let hand = []
  let board = []
  let reach = 1
  let distance = 0
  let character = null
  let life = 0
  let maxlife = 0

  return {
    name,
    role,
    hand,
    board,
    reach,
    distance,
    character,
    life,
    maxlife
  }
}

export const module = {
  namespaced: true,
  state: {
    matchid: null,
    players: {},
    turns: [],
    you: null,
    turn: null,
    viewed: null,
    revealed: [],
    discards: [],
    ready: false
  },
  getters: {
    players(_state) {
      return _state.turns.map(el => _state.players[el])
    },
    you(_state) {
      return _state.players[_state.you]
    },
    current_player(_state) {
      return _state.players[_state.turn]
    },
    viewed_player(_state) {
      return _state.players[_state.viewed]
    },
    viewed_distance(_state) {
      let distances = {}
      let turns = _state.turns.filter(el => _state.players[el].life > 0)
      let tv = turns.indexOf(_state.viewed)
      
      for (let turn = 0; turn < turns.length; ++turn) {
        distances[turns[turn]] = _state.players[turns[turn]].distance + Math.min(turns.length - Math.abs(tv - turn), Math.abs(tv - turn))
      }

      turns = _state.turns.filter(el => _state.players[el].life == 0)
      for (let turn of turns) {
        distances[turn] = 0
      }

      return distances
    },
    you_distance(_state) {
      let ty = _state.turns.indexOf(_state.you)
      let tv = _state.turns.indexOf(_state.viewed)

      return _state.players[_state.viewed].distance + Math.min((tv + ty) % _state.turns.length, Math.abs(tv - ty))
    },
    in_game(_state) {
      return _state.ready
    }
  },
  mutations: {
    init(_state, _data) {
      _state.you = _data.you
      _state.viewed = _data.you

      for (let p of _data.match.players) {
        Vue.set(_state.players, p, player(p))
      }
      _state.matchid = _data.match.id
    },
    set_start_data(_state, _data) {
      _state.turns = _data.turns
      _state.turn = _data.turn
      for (let player of _data.players) {
        _state.players[player.name].character = player.character
        _state.players[player.name].life = player.life
        _state.players[player.name].maxlife = player.maxlife
        _state.players[player.name].hand = player.hand
        _state.players[player.name].board = player.board
        _state.players[player.name].role = player.role
      }
      _state.discards = _data.discards
      _state.revealed = _data.revealed

      _state.ready = true
    },
    edit_hand(_state, _data) {
      let player = _state.players[_data.player]

      for (let card of _data.new_cards) {
        player.hand.push(card)
      }
    },
    // from:player, to, card, position
    play_card(_state, _data) {
      let i = _state.players[_data.from].hand.findIndex(card => card.pid == _data.pid) // or from the board
      // TODO check i

      let card = _state.players[_data.from].hand[i]
      card.hid = _data.hid
      _state.players[_data.to].board.push(card)
      
      Vue.nextTick(() => Vue.delete(_state.players[_data.from].hand, i))
    },
    reveal_cards(_state, _data) {
      _state.revealed = _data.cards
    },
    card_picked(_state, _data) {
      let i = _state.revealed.findIndex(card => card.pid == _data.pid)
      if (i !== -1) {
        let card = _state.revealed[i]
        _state.players[_data.player].hand.push(card)
      }

      Vue.nextTick(() => Vue.delete(_state.revealed, i))
    },
    ////////////////////////////////
    //// V 0.1
    ////////////////////////////////
    move_card(_state, _data) {
      let owner = _data.from.split('/')
      if (owner[0] == 'deck') {
        // pass
      } else if (owner[0] == 'discards') {
        for (let i = _state.discards.length - 1; i >= 0; i--) {
          if (_state.discards[i].pid == _data.card.pid) {
            Vue.delete(_state.discards, i)

            break
          }
        }
      } else if (owner[0] == 'revealed') {
        for (let i = _state.revealed.length - 1; i >= 0; i--) {
          if (_state.revealed[i].pid == _data.card.pid) {
            Vue.delete(_state.revealed, i)

            break
          }
        }
      } else if (owner[0] == 'hand') {
        let p = _state.players[owner[1]]
        let i = p.hand.findIndex(card => card.pid == _data.card.pid)
        Vue.nextTick(() => Vue.delete(_state.players[owner[1]].hand, i))
      } else if (owner[0] == 'board') {
        let p = _state.players[owner[1]]
        let i = p.board.findIndex(card => card.pid == _data.card.pid)
        Vue.nextTick(() => Vue.delete(_state.players[owner[1]].board, i))
      }
      
      let target = _data.to.split('/')
      if (target[0] == 'deck') {
        return
      } else if (target[0] == 'discards') {
        _state.discards.push(_data.card)
      } else if (target[0] == 'revealed') {
        _state.revealed.push(_data.card)
      } else if (target[0] == 'hand') {
        _state.players[target[1]].hand.push(_data.card)
      } else if (target[0] == 'board') {
        _state.players[target[1]].board.push(_data.card)
      }
    },
    shuffle(_state) {
      _state.discards = []
    },
    set_life(_state, _data) {
      _state.players[_data.player.name].life = _data.player.life
    },
    set_turn(_state, _data) {
      _state.turn = _data.turn
      _state.viewed = _data.turn
    },
    reveal_role(_state, _data) {
      _state.players[_data.player].role = _data.role
    }
  },
  actions: {
    _set_viewed_player(_ctx, _name) {
      _ctx.state.viewed = _name
    },
    _init(_ctx, _data) {
      if (_ctx.state.ready == false) {
        _data.you = _ctx.rootState.user
        _ctx.commit('init', _data)
  
        APIRequest(_ctx, 'p_get_start_data', {'matchid': _ctx.state.matchid}).then((_r) => {
          _ctx.commit('set_start_data', _r)
        })
  
        ////////////////////////////////
        //// V 0.1
        ////////////////////////////////
        APIAddEventListener(_ctx, 'card_moved', (_r) => {
          _ctx.commit('move_card', _r)
        })
        APIAddEventListener(_ctx, 'deck_shuffled', () => {
          _ctx.commit('shuffle')
        })
        APIAddEventListener(_ctx, 'set_life', (_r) => {
          _ctx.commit('set_life', _r)
        })
        APIAddEventListener(_ctx, 'set_turn', (_r) => {
          _ctx.commit('set_turn', _r)
        })
        APIAddEventListener(_ctx, 'reveal_role', (_r) => {
          _ctx.commit('reveal_role', _r)
        })
      }
    },
    _drawCards(_ctx) {
      APIRequest(_ctx, 'p_draw', {'matchid': _ctx.state.matchid, 'amount': 1}).then((_r) => {
        _ctx.commit('edit_hand', _r)
      })
    },
    // to:player/board, card:card, ?position:(x,y)
    _playCard(_ctx, _data) {
      _data['matchid'] = _ctx.state.matchid

      return APIRequest(_ctx, 'p_play', _data).then((_r) => {
        _ctx.commit('play_card', _r)
      })
    },
    _revealCards(_ctx, _data) {
      _data['matchid'] = _ctx.state.matchid
      _data['amount'] = 1

      return APIRequest(_ctx, 'p_reveal', _data).then((_r) => {
        _ctx.commit('reveal_cards', _r)
      })
    },
    _pickRevealed(_ctx, _data) {
      _data['matchid'] = _ctx.state.matchid

      return APIRequest(_ctx, 'p_pick_revealed', _data).then((_r) => {
        _ctx.commit('card_picked', _r)
      })
    },
    /*_endTurn(_ctx, _data) {

    }*/
    ////////////////////////////////////////////////////////////////
    //// V 0.1
    ////////////////////////////////////////////////////////////////
    _moveCard(_ctx, _data) {
      _data['matchid'] = _ctx.state.matchid
      console.log("moving card")
      return APIRequest(_ctx, 'p_move_card', _data).then((_r) => {
        console.log("moved card: ", _r)
        _ctx.commit('move_card', _r)
      }).catch((_r) => {
        if (_r.status === 818) {
          pushError(_ctx, "Empty deck")
        }
      })
    },
    _shuffle(_ctx, _data) {
      _data['matchid'] = _ctx.state.matchid

      return APIRequest(_ctx, 'p_shuffle', _data).then(() => {
        _ctx.commit('shuffle')
      })
    },
    _setLife(_ctx, _data) {
      _data['matchid'] = _ctx.state.matchid
      
      return APIRequest(_ctx, 'p_set_life', _data).then((_r) => {
        _ctx.commit('set_life', _r)
      })
    },
    _passTurn(_ctx) {
      return APIRequest(_ctx, 'p_pass_turn', {'matchid': _ctx.state.matchid}).then((_r) => {
        _ctx.commit('set_turn', _r)
      })
    }
  }
}