<template>
  <div class="cmp-discards">
    <div v-if="expanded && discards.length > 1" class="cmp-other-cards">
      <div><div>
        <interaction v-for="el in discards.slice(0, discards.length - 1)" :key="el.pid" :actions="[{
          text: 'pick',
          action: '_moveCard',
          data: {
            from: 'discards',
            to: 'hand/' + you.name,
            hid: el.hid
          },
          if: discards.length > 0
        }]">
          <card :data="el" />
        </interaction>
      </div></div>
    </div>
    <interaction :actions="[{
        text: 'pick',
        action: '_moveCard',
        data: {
          from: 'discards',
          to: 'hand/' + you.name,
          hid: discards.length > 0 ? discards[discards.length - 1].hid : 0
        },
        if: discards.length > 0
      }, {
        text: 'shuffle',
        action: '_shuffle',
        data: {}
      }]">
      <img v-if="discards.length == 0" :src="require('@/assets/imgs/card-discard.png')">
      <card @click.native="expanded = !expanded" v-else :data="discards[discards.length - 1]" style="positoin: relative; bottom: 4px;"/>
    </interaction>
  </div>
</template>

<script>

import { mapState, mapGetters } from 'vuex'

import Interaction from './Interaction'
import Card from './Card'

export default {
  data: function() {
    return {
      expanded: false
    }
  },
  components: {
    Interaction, Card
  },
  computed: {
    ...mapState('game/match', ['discards']),
    ...mapGetters('game/match', ['you'])
  }
}

</script>

<style scoped>

.cmp-discards {
  position: relative;
}

img {
  display: inline-block;
  width: 206px;
  margin-left: 8px;
  filter: drop-shadow(-1px 5px 10px #000);
}

.cmp-other-cards {
  position: absolute;
  right: 100%;
  margin-right: 16px;
  opacity: 0.8;
  overflow-y: hidden;
  height: 294px;
  transform: scaleX(-1);
}

.cmp-other-cards > div {
  width: 1024px;
  padding-right: 512px;
  overflow-x: scroll;
}

.cmp-other-cards > div > div {
  display: flex;
  flex-shrink: 0;
  flex-flow: row-reverse;
  width: min-content;
  height: 294px;
}

.cmp-other-cards > div > div > * {
  margin-right: -48px;
  transform: scaleX(-1);
}

</style>