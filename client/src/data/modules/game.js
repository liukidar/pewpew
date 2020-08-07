import Vue from 'vue'
import { module as match } from './match'
import { e, APIRequest, APIAddEventListener, APIRemoveEventListener } from '../api'
import { pushError } from '../msgmanager'

export const module = {
  namespaced: true,
  modules: {
    match
  },
  state: {
    user: null,
    selected_match: null,
    matches: {},
    cards: {}
  },
  getters: {
    card_info(_state) {
      return (card) => card.hid ? _state.cards[card.hid] : {}
    },
    get_matches(_state) {
      return _state.matches
    },
    get_active_match(_state) {
      return _state.matches[_state.selected_match]
    }
  },
  mutations: {
    load_cards(_state, _data) {
      for (let card of _data.cards) {
        Vue.set(_state.cards, card.hid, card)
      }
    },
    edit_match(_state, _data) {
      Vue.set(_state.matches, _data.match.id, _data.match)
    },
    list_matches(_state, _data) {
      _state.matches = _data.matches
    },
    join_match(_state, _data) {
      _state.selected_match = _data.match.id
    },
    leave_match(_state) {
      _state.selected_match = null
    }
  },
  actions: {
    _loadCards(_ctx) {
      return APIRequest(_ctx, 'load_cards', {}).then((_r) => {
        _ctx.commit('load_cards', _r)
      })
    },
    _createMatch(_ctx, _data) {
      return APIRequest(_ctx, 'create_match', _data).then((_r) => {
        _ctx.commit('join_match', _r)
        _ctx.commit('edit_match', _r)
        APIAddEventListener(_ctx, 'match_edit', (r) => {
          _ctx.commit('edit_match', r)
          if (r.match.status == 'ready') {
            _ctx.dispatch('match/_init', r)
          }
        })

        return _r
      })
    },
    _listMatches(_ctx) {
      return APIRequest(_ctx, 'list_matches', {}).then((_r) => {
        _ctx.commit('list_matches', _r)
      })
    },
    _joinMatch(_ctx, _data) {
      return APIRequest(_ctx, 'join_match', _data).then((_r) => {
        _ctx.commit('join_match', _r)
        _ctx.commit('edit_match', _r)
        if (_r.match.status == 'ready') {
          _ctx.dispatch('match/_init', _r)
        } else {
          APIAddEventListener(_ctx, 'match_edit', (r) => {
            _ctx.commit('edit_match', r)
            if (r.match.status == 'ready') {
              _ctx.dispatch('match/_init', r)
            }
          })
        }
        return _r
      }).catch((_r) => {
        if (_r.status == e["ERR_MATCH_PASSWORD_INVALID"]) {
          pushError(_ctx, "Invalid password")
        }
        else if (_r.status == e["ERR_MATCH_NOT_EXIST"] || _r.status == e["ERR_MATCH_NOT_OPEN"]) {
          pushError(_ctx, "Can't join network")
          _ctx.dispatch('_listMatches')
        }

        throw _r
      })
    },
    _leaveMatch(_ctx) {
      return APIRequest(_ctx, 'leave_match', {}).finally(() => {
        _ctx.commit('leave_match')
        APIRemoveEventListener(_ctx, 'match_edit')
        _ctx.dispatch('_listMatches')
      })
    },
    _startMatch(_ctx) {
      return APIRequest(_ctx, 'start_match', { matchid: _ctx.getters.get_active_match.id }).catch((_r) => {
        if (_r.status == e["ERR_MATCH_NOT_READY"]) {
          pushError(_ctx, "Not enough players")
        }
        throw _r
      })
    }
  }
}