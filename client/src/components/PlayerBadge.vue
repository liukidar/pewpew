<template>
  <div @click="setViewedPlayer()" class="cmp-player-badge modal" :class="{active: current_player == data}">
    <img-btn v-if="data == you" @click="this._passTurn" class="cmp-turn-btn" src="turn" />
    <img v-if="viewed_player == data" :src="require('@/assets/imgs/paper-badge-viewed.png')" />
    <img v-else :src="require('@/assets/imgs/paper-badge.png')" />
    <div class="modal-body">
      <img class="cmp-role-icon" :src="require('@/assets/imgs/icon-' + data.role + '.png')" />
      <life :data="data" class="horizontal" />
      <div style="width: 105px;"></div>
      <sign class="cmp-reach" :s="data.reach" />
      <sign class="cmp-distance" :s="viewed_distance[data.name]" />
      <sign class="cmp-cards" :s="data.hand.length" />
    </div>
    <div class="cmp-name">
      {{data.name}}
    </div>
  </div>
</template>

<script>

import { mapGetters, mapActions } from 'vuex'
import Sign from './Sign'
import Life from './Life'
import ImgBtn from './ImgBtn'

export default {
  props: ['data'],
  computed: {
    ...mapGetters('game/match', ['current_player', 'viewed_player', 'viewed_distance', 'you'])
  },
  methods: {
    ...mapActions('game/match', ['_set_viewed_player', '_passTurn']),
    setViewedPlayer() {
      if (this.data.life) this._set_viewed_player(this.data.name)
    }
  },
  components: {
    Sign, Life, ImgBtn
  }
}
</script>

<style scoped>

.cmp-player-badge {
  width: 346px;
  margin: 4px -8px;
  transform: translateX(0);
  transition: transform .5s;
  cursor: pointer;
  pointer-events: all;
}
.cmp-player-badge > img {
  filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.5));
}

.cmp-player-badge.active {
  transform: translateX(64px);
}

.cmp-turn-btn {
  position: absolute;
  top: 32px;
  right: 100%;
}

.cmp-life {
  position: absolute;
  top: 30px;
  left: 166px;
  width: 34px;
  pointer-events: none;
}

.cmp-role-icon {
  position: absolute;
  top: 21px;
  left: 15px;
  width: 48px;
}

.cmp-reach {
  position: absolute;
  left: 191px;
  top: 39px;
  transform: scale(2);
}

.cmp-distance {
  transform: scale(2);
  position: absolute;
  left: 243px;
  top: 54px;
}

.cmp-cards {
  position: absolute;
  left: 313px;
  top: 32px;
  transform: scale(2);
}

.cmp-name {
  position: absolute;
  left: 64px;
  top: -6px;
  font-family: 'Western';
  font-size: 18px;
  letter-spacing: 1px;
  text-overflow: ellipsis;
  color: #fff;
  width: 196px;
  overflow: hidden;
  text-align: left;
  text-shadow: 2px 2px 2px rgba(0,0,0,0.8);
}

</style>