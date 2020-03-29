<template>
  <div @click="setViewedPlayer()" class="cmp-player-badge-big modal">
    <img :src="require('@/assets/imgs/paper-badge-big.png')">
    <div class="modal-body">
      <life :data="you" />
      <img class="cmp-role-icon" :src="require('@/assets/imgs/icon-' + you.role + '.png')" />
      <sign class="cmp-distance" :s="you_distance" />
      <sign class="cmp-reach" :s="you.reach" />
      <sign class="cmp-cards" :s="you.hand.length" />
      <div class="cmp-name signature">{{you.name}}</div>
    </div>
  </div>
</template>

<script>

import { mapGetters, mapActions } from 'vuex'
import Sign from './Sign'
import Life from './Life'

export default {
  props: ['data'],
  computed: {
    ...mapGetters('game/match', ['you', 'you_distance'])
  },
  methods: {
    ...mapActions('game/match', ['_set_viewed_player']),
    setViewedPlayer() {
      this._set_viewed_player(this.you.name)
    }
  },
  components: {
    Sign, Life
  }
}
</script>

<style scoped>

.cmp-player-badge-big {
  width: 280px;
}

.cmp-player-badge-big > img {
  filter: drop-shadow(-1px 5px 10px #000);
}

.cmp-life {
  position: absolute;
  width: 54px;
  top: 48px;
  left: 78px;
}

.cmp-role-icon {
  width: 48px;
  position: absolute;
  top: 85px;
  left: 167px;
}

.cmp-distance {
  width: 18px;
  position: absolute;
  left: 68px;
  top: 244px;
}

.cmp-reach {
  width: 18px;
  position: absolute;
  left: 130px;
  top: 232px;
}

.cmp-cards {
  width: 18px;
  position: absolute;
  left: 209px;
  top: 224px;
}

.cmp-name {
  position: absolute;
  top: 304px;
  left: 142px;
  font-size: 28px;
  text-overflow: ellipsis;
  text-transform: capitalize;
  width: 132px;
  overflow: hidden;
  text-align: left;
  padding-left: 8px;
  border-bottom: 1px solid #000;
}

</style>