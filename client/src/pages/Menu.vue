<template>
  <div class="cmp-menu" :style="{backgroundImage: 'url(' + require('@/assets/imgs/main-board.png') + ')'}">
    <div class="scroll-wrapper">
      <div class="cmp-pivot">
        <!-- MAIN MENU -->
        <transition appear name="main-title">
          <div v-if="!user" class="cmp-title modal">
            <div class="modal-body v-flex center">
              <h1 class="title">(PEW-PEW)</h1>
              <h3 class="title" style="padding-left: 256px;">ONLINE VERSION!</h3>
              <br><br>
            </div>
          </div>
        </transition>
        <!-- REGISTER MENU -->
        <transition appear name="register">
          <div v-if="!user" class="cmp-register modal">
            <img :src="require('@/assets/imgs/paper-big.png')">
            <div class="modal-body left-align">
              <div class="f-left">
                <h2 class="title">Pick a username</h2>
                <br>
                <input v-model="username" spellcheck="false" class="signature" type="text">
              </div>
              <div class="f-right">
                <br><br><br><br>
                <a @click="register()" class="submit-btn"></a>
              </div>
              <div class="f-clear"></div>
            </div>
          </div>
        </transition>
        <!-- MATCH LIST MENU -->
        <transition name="match-list">
          <div v-if="user && !active_match" class="cmp-match-list left-align">
            <br>
            <!-- Create match -->
            <h2 class="title white-text">HEY {{user}}!</h2>
            <br>
            <div class="modal">
              <img :src="require('@/assets/imgs/paper-horizontal.png')">
              <div class="modal-body">
                <br>
                <div class="f-left">
                  <h2 class="title">Create a game</h2>
                  <br>
                  <p>
                    <input v-model="createMatchName" :placeholder="createMatchNamePlaceholder" class="signature small" type="text">
                    <input v-model="createMatchPassword" placeholder="Password" style="margin-left: 64px;" class="signature small" type="password">
                  </p>
                  <p class="title">
                    <br><br>
                    VERSION: 0.0
                  </p>
                </div>
                <div class="f-right">
                  <br><br><br><br>
                  <a @click="createMatch()" class="submit-btn"></a>
                </div>
                <div class="f-clear"></div>
              </div>
            </div>
            <br>
            <!-- Match list -->
            <h2 class="title white-text">Or join one: </h2>
            <br>
            <div style="position: relative;">
              <img-btn @click="this._listMatches" class="refresh-btn" src="refresh">REFRESH!</img-btn>
              <tr-slide-in :stagger="100" :settings="{from: '100vw, 0%'}">
                <div class="modal" v-for="(match, index) in matches" :data-index="index + 1" :key="match.id">
                  <img :src="require('@/assets/imgs/paper-horizontal-thin.png')">
                  <div class="modal-body">
                    <h4 class="title">{{match.owner}}'s Game</h4>
                    <br>
                    <h2 class="title">
                      {{match.name}}
                      <small><small>
                        <div>
                          <p style="margin-top: 8px" class="grey-text f-left">VERSION: 0.0 - PLAYERS: {{match.players.length}}</p>
                          <img-btn src="gun" offset="24" @click="joinMatch(match)" class="f-right">JOIN!</img-btn>
                        </div>
                      </small></small>
                    </h2>
                  </div>
                </div>
              </tr-slide-in>
              <transition name="fade">
                <div v-if="!Object.keys(matches).length" class="modal" style="position: absolute; top: 0; left: 0;">
                  <img :src="require('@/assets/imgs/paper-horizontal-thin.png')">
                  <div class="modal-body">
                    <h2 class="title">
                      No match found...
                    </h2>
                  </div>
                </div>
              </transition>
            </div>
          </div>
        </transition>
        <!-- MATCH MENU -->
        <transition appear name="match">
          <div v-if="active_match" class="cmp-match modal">
            <img :src="require('@/assets/imgs/paper-vertical-large.png')">
            <div class="modal-body">
              <div @click="leaveMatch()" class="modal-close"></div>
              <div class="h-flex center">
                <h1 class="title"><small>(</small></h1>
                <h2 class="title">{{active_match.name}}</h2>
                <h1 class="title"><small>)</small></h1>
              </div>
              <div class="left-align">
                <div class="h-flex center space-between">
                  <div>
                    <br><br>
                    <h3 class="title">{{active_match.owner}}'S GAME</h3>
                    <h4 class="title"><small>{{user}}</small></h4>
                    <br><br>
                  </div>
                  <img-btn v-show="user == active_match.owner" @click="startMatch" src="gun" offset="24" class="x1_5">GO!</img-btn>
                </div>
                <h4 class="title">PLAYERS<span class="slash"/>9</h4>
                <div class="hr"></div>
                <table>
                  <tbody>
                    <tr class="title" v-for="(player, index) in active_match.players" :key="index">
                      <td>@ {{index + 1}}.</td><td>{{player}}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>

import { mapState, mapGetters, mapActions } from 'vuex'
import TrSlideIn from '../components/TrSlideIn'
import ImgBtn from '../components/ImgBtn'

export default {
  data: function () {
    return {
      username: null,
      createMatchNamePlaceholder: 'High Noon in Ruby City',
      createMatchName: null,
      createMatchPassword: null
    }
  },
  computed: {
    ...mapState(['user']),
    ...mapGetters(['msgs']),
    ...mapGetters('game', {matches: 'get_matches', active_match: 'get_active_match'})
  },
  methods: {
    ...mapActions(['_register']),
    ...mapActions('game', ['_loadCards', '_createMatch', '_listMatches', '_joinMatch', '_leaveMatch', '_startMatch']),
    ...mapActions('game/match', {initMatch: '_init'}),
    register() {
      if (this.username) {
        this._register({ username: this.username }).then(() => {
          this._loadCards()
          this._listMatches()
        })
      } else {
        this.msgs.pushError('Username required')
      }
    },
    createMatch() {
      let matchName = this.createMatchName ? this.createMatchName : this.createMatchNamePlaceholder
      this._createMatch({matchname: matchName, matchpassword: this.createMatchPassword})
    },
    joinMatch(_match) {
      // TODO password
      this._joinMatch({matchid: _match.id, matchpassword: 'brucoluco_xd'})
    },
    leaveMatch() {
      this._leaveMatch().then(() => {
        this._listMatches()
      })
    },
    startMatch() {
      this._startMatch()
    }
  },
  components: {
    TrSlideIn, ImgBtn
  }
}
</script>

<style scoped>

.modal {
  width: 100%;
}

.cmp-menu {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
.cmp-pivot {
  position: relative;
  width: 892px;
  height: 100%;
  margin: 0 auto;
}
.scroll-wrapper {
  margin-right: -18px;
  height: 100%;
  box-sizing: border-box;
  overflow-y: scroll;
  overflow-x: hidden;
}

.cmp-title {
  position: absolute;
  top: 120px;
  height: 512px;
  color: #FFF;
  text-shadow: 4px 8px 8px #000;
}

.cmp-register {
  transform: rotateZ(-16deg);
  position: absolute;
  bottom: -200px;
}
.cmp-register > div {
  padding: 64px 128px;
}

.cmp-match-list {
  padding-top: 120px;
}
.cmp-match-list .modal {
  margin-bottom: 40px;
}
.cmp-match-list .modal-body {
  padding: 48px;
}

.cmp-match {
  position: absolute;
  top: 200px;
  width: 562px;
  margin: 0 165px;
}

.cmp-match .modal-body {
  padding: 80px;
}

td {
  padding: 8px 4px;
}
td:first-child {
  width: 64px;
}

.refresh-btn {
  position: absolute;
  right: 46px;
  top: 32px;
  z-index: 1;
}

/* TRANSITIONS */
.main-title-enter-active, .main-title-leave-active {
  transition: transform 1s ease;
}
.main-title-enter, .main-title-leave-to {
  transform: translateY(-100vh);
}

.register-enter-active {
  transition: transform .5s 1s;
}
.register-leave-active {
  transition: transform .5s
}
.register-enter, .register-leave-to {
  transform: translate(0vw, 100vh) scale(0.8) rotateZ(20deg);
}

.match-list-enter-active, .match-list-leave-active {
  transition: transform 1s ease;
}
.match-list-enter, .match-list-leave-to {
  transform: translateX(100vw);
}

.match-enter-active, .match-leave-active {
  transition: transform 1s ease;
}
.match-enter, .match-leave-to {
  transform: translateX(-100vw);
}

</style>