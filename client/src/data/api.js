import uuid4 from 'uuid4'

export const e = {
  ERR_USERNAME_NOT_FOUND: 808, 
  ERR_TAKEN_USERNAME: 809,
  ERR_OVERFLOW_PLAYERS_NUMBER: 810, 
  ERR_MATCH_OWNED: 811,
  ERR_MATCH_NOT_OPEN: 812,
  ERR_MATCH_NOT_EXIST: 813,
  ERR_USER_NOT_IN_MATCH: 814,
  ERR_NOT_MATCH_OWNER: 815,
  ERR_MATCH_PASSWORD_INVALID: 816,
  ERR_MATCH_NOT_READY: 817
}

export function APIRequest(_ctx, _action, _data) {
  _data.action = _action
  
  return new Promise((resolve, reject) => {
    _ctx.rootState.api.request(_data, (r) => {
      if (r.status == 200) {
        return resolve(r)
      } else {
        return reject(r)
      }
    })
  })
}

export function APISetCookie(_ctx, _cookie, _data) {
  _ctx.rootState.api.setCookie(_cookie, _data)
}

export function APIAddEventListener(_ctx, _event, _callback) {
  _ctx.rootState.api.addEventListener(_event, _callback)
}

export function APIRemoveEventListener(_ctx, _event) {
  _ctx.rootState.api.removeEventListener(_event)
}

export function API() {
  let websocket = null
  let promises = {}
  let cookies = {}
  let eventListeners = {}

  function setCookie(_cookie, _data) {
    cookies[_cookie] = _data
  }

  function addEventListener(_event, _callback) {
    if (eventListeners[_event]) {
      console.error("CALLBACK ALREADY EXISTS")
    }
    eventListeners[_event] = _callback
  }

  function removeEventListener(_event) {
    delete eventListeners[_event]
  }

  function request(_data, _callback) {
    for (let cookie in cookies) {
      _data[cookie] = cookies[cookie]
    }
    _data.requestId = uuid4()
    promises[_data.requestId] = _callback
    websocket.send(JSON.stringify(_data))
  }


  // Requesting ws server ip address
  websocket = new WebSocket('ws://' + window.location.hash.substr(1))
  websocket.addEventListener('message', (e) => {
    let r = JSON.parse(e.data)
    console.log(r)
    console.log("log: ", promises)
    if (r.event) {
      let listener = eventListeners[r.event]
      if (listener) {
        listener(r)
      }
    }
    if (r.auth) {
      setCookie('auth', r.auth)
    } else if (promises[r.requestId]) {
      promises[r.requestId](r)
      delete promises[r.requestId]
    }
  })

  return {
    setCookie,
    addEventListener,
    removeEventListener,
    request
  }
}
