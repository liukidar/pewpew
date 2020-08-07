<template>
  <div id="app">
    <sprite isrc="gun-shot" />
    <sprite isrc="card-yellow.png" scale="3.5" onclick="setAnimation(bang)"/>
    <page-menu v-if="!in_game" />
    <page-match v-if="in_game" />
    <msg-manager />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import MsgManager from './components/MsgManager.vue'
import PageMenu from './pages/Menu'
import PageMatch from './pages/Match'
import Sprite from './components/Sprite'

export default {
  name: 'App',
  computed: {
    ...mapGetters('game/match', ['in_game'])
  },
  methods: {
    ...mapActions('game', { registerUser: '_register'})
  },
  components: {
    PageMenu, PageMatch, MsgManager, Sprite
  }
}
</script>

<style>
@import './lib/css/style.css';

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  background: #8C5325;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
</style>
