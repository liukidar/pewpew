import Vue from 'vue'
import Vuex from 'vuex'
import { APIRequest, e } from './api.js'
import { MsgManager, pushError } from './msgmanager'
import { module as game } from './modules/game'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    user: null,
    //api: API(),
    msgmanager: MsgManager(),
    resources: {}
  },
  getters: {
    msgs(_state) {
      return _state.msgmanager
    },
    connected(_state) {
      return _state.api.connected
    }
  },
  mutations: {
    register(_state, _data) {
      _state.user = _data.username
    }
  },
  actions: {
    // username:string
    _register(_ctx, _data) {
      return APIRequest(_ctx, 'register', _data).then((_r) => {
        _ctx.commit('register', _r)
      }).catch((_r) => {
        if (_r.status == e["ERR_TAKEN_USERNAME"]) {
          pushError(_ctx, "Username already taken!")
        }

        throw _r
      })
    },
  },
  modules: {
    game
  }
})