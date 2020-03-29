<template>
  <div id="app">
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

export default {
  name: 'App',
  computed: {
    ...mapGetters('game/match', ['in_game'])
  },
  methods: {
    ...mapActions('game', { registerUser: '_register'})
  },
  components: {
    PageMenu, PageMatch, MsgManager
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
