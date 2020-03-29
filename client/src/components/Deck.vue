<template>
  <div class="cmp-deck">
    <interaction
      :actions="[{
        text: 'draw',
        action: '_moveCard',
        data: {
          from: 'deck',
          to: 'hand/' + you.name
        }
      }, {
        text: 'reveal',
        action: '_moveCard',
        data: {
          from: 'deck',
          to: 'revealed'
        }
      }]">
      <img :src="require('@/assets/imgs/card-background.png')">
    </interaction>
  </div>
</template>

<script>

import { mapGetters } from 'vuex'

import Interaction from './Interaction'

export default {
  components: {
    Interaction
  },
  computed: {
    ...mapGetters('game/match', ['you'])
  }
}
</script>

<style scoped>

img {
  display: inline-block;
  width: 206px;
  margin-left: 8px;
  filter: drop-shadow(-1px 5px 10px #000);
}

</style>