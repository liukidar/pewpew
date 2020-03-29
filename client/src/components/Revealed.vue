<template>
  <div v-if="revealed.length" class="cmp-revealed h-flex center">
    <div v-for="el in revealed" :key="el.pid">
      <interaction :actions="[{
          text: 'pick',
          action: '_moveCard',
          data: {
            from: 'revealed',
            to: 'hand/' + you.name,
            'hid': el.hid
            }
          },{
          text: 'discard',
          action: '_moveCard',
          data: {
            from: 'revealed',
            to: 'discards',
            'hid': el.hid}
        }]">
        <card :data="el" />
      </interaction>
    </div>
  </div>
</template>

<script>

import { mapState, mapGetters } from 'vuex'
import Interaction from './Interaction'
import Card from './Card'

export default {
  computed: {
    ...mapState('game/match', ['revealed']),  
    ...mapGetters('game/match', ['you'])
  },
  components: {
    Card, Interaction
  }
}
</script>

<style scoped>

.cmp-revealed {
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  position: relative;
  padding: 0 256px 0 396px;
  box-sizing: border-box;
}

.cmp-card {
  margin-right: 16px;
  margin-bottom: 16px;
}

</style>