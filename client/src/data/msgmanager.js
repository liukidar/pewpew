export function pushInfo(_ctx, _msg, _duration) {
  _duration = _duration || 2000
  _ctx.rootState.msgmanager.pushInfo(_msg, _duration)
}

export function pushError(_ctx, _msg, _duration) {
  _duration = _duration || 2000
  _ctx.rootState.msgmanager.pushError(_msg, _duration)
}

export function MsgManager() {
  let msgs = []
  let i = 0

  function pushInfo(_msg, _duration) {
    _duration = _duration || 2000
    let m = { id: i++, text: _msg, type: 'info', remove: () => { let i = msgs.indexOf(m); if (i !== -1) msgs.splice(i, 1)} }
    msgs.push(m)
    setTimeout(m.remove, _duration)
  }

  function pushError(_msg, _duration) {
    _duration = _duration || 2000
    let m = { id: i++, text: _msg, type: 'warning', remove: () => { let i = msgs.indexOf(m); if (i !== -1) msgs.splice(i, 1)} }
    msgs.push(m)
    setTimeout(m.remove, _duration)
  }

  return {
    msgs,
    pushInfo,
    pushError,
  }
}