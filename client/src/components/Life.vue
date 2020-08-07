<template>
  <div class="cmp-life">
    <div><img @click="setLife(data.life - index - 1)" :src="require('@/assets/imgs/life.png')" v-for="(el, index) in data.life" :key="index"></div>
    <div><img @click="setLife(data.maxlife - index)" :src="require('@/assets/imgs/not-life.png')" v-for="(el, index) in (data.maxlife - data.life)" :key="index"></div>
  </div>
</template>

<script>

import { mapActions } from 'vuex'

export default {
  props: ['data'],
  methods: {
    ...mapActions('game/match', ['_setLife']),
    setLife(_amount) {
      this._setLife({'life': _amount})
    }
  }
}
</script>

<style scoped>

.cmp-life {
  display: flex;
  flex-flow: column-reverse;
  transform-origin: 0% 0%;
}

.cmp-life > div {
  width: 100%;
}

.cmp-life.horizontal {
  transform: scaleX(-1) rotate(90deg) scaleY(-1);
}

img {
  width: 100%;
  display: block;
  padding: 2px 0;
}

</style>