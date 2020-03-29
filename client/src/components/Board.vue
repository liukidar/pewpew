<template>
  <div class="cmp-board" :style="{backgroundPosition: 'top 0px left ' + offsetX, backgroundImage: 'url(' + require('@/assets/imgs/main-board.png') + ')'}">
    <div class="cmp-cards-wrapper" :class="{opponent: viewed_player != you}">
      <div class="cmp-card-wrapper" v-for="(el, index) in viewed_player.board" :key="index" style="position: absolute; transform: translateX(-50%)" :style="{bottom: el.bottom, left: el.left}">
        <interaction :actions="[{
            text: 'discard',
            action: '_moveCard',
            data: {
              from: 'board/' + viewed_player.name,
              to: 'discards',
              'hid': el.hid
            }
          },{
            text: 'pick',
            action: '_moveCard',
            data: {
              from: 'board/' + viewed_player.name,
              to: 'hand/' + you.name,
              'hid': el.hid
            }
          }]">
          <card :data="el" :class="{reversed: viewed_player != you}"></card>
        </interaction>
      </div>
    </div>
    <slot></slot>
  </div>
</template>

<script>

import { mapGetters } from 'vuex'
import Card from './Card'
import Interaction from './Interaction'

export default {
  data: function () {
    return {
      cards: [],
      offsetX: Math.floor(Math.random() * 100) + '%'
    }
  },
  computed: {
    ...mapGetters('game/match', ['viewed_player', 'you'])
  },
  components: {
    Card, Interaction
  }
}
</script>

<style scoped>

.cmp-board {
  position: relative;
}


.cmp-cards-wrapper {
  position: absolute;
  bottom: 0;
  left: 50%;
}
.cmp-cards-wrapper.opponent {
  transform: scale(-1);
  top: -100px;
  bottom: auto;
}


.cmp-card-wrapper:hover {
  z-index: 1;
}

</style>