<template>
  <div class="cmp-match">
    <div class="right-col">
      <board>
        <hand />
        <revealed />
        <discards />
        <deck />
        <player-badge-big />
      </board>
    </div>
    <div class="left-col modal" :style="{backgroundImage: 'url(' + require('@/assets/imgs/cloth-bkg.png') + ')'}">
      <player-badge v-for="player in players" :key="player.name" :data="player" />
      <card :data="you.character" />
    </div>
  </div>
</template>

<script>

import { mapGetters } from 'vuex'

import Hand from '../components/Hand'
import Board from '../components/Board'
import PlayerBadge from '../components/PlayerBadge'
import PlayerBadgeBig from '../components/PlayerBadgeBig'
import Deck from '../components/Deck'
import Discards from '../components/Discards'
import Revealed from '../components/Revealed'
import Card from '../components/Card'

export default {
  props: {
    msg: String
  },
  computed: {
    ...mapGetters('game/match', ['you', 'players', 'viewed_player'])
  },
  components: {
    Board, Hand, PlayerBadge, PlayerBadgeBig, Deck, Revealed, Discards, Card
  }
}
</script>

<style scoped>

.cmp-match {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
}

.left-col {
  padding: 14px 36px 0 0;
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background-repeat: repeat-y;
  background-size: fill;
  pointer-events: none;
}

.left-col .cmp-card {
  position: absolute;
  bottom: -128px;
  left: 24px;
  transition: bottom .5s;
  pointer-events: all;
}
.left-col .cmp-card:hover {
  bottom: 48px;
}

.right-col {
  height: 100%;
}

.cmp-board {
  height: 100%;
}

.cmp-player-badge-big {
  position: absolute;
  right: 0;
  top: 96px;
}

.cmp-deck {
  position: absolute;
  bottom: 64px;
  right: -64px;
}

.cmp-discards {
  position: absolute;
  bottom: 64px;
  right: 148px;
}

</style>
