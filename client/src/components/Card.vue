<template>
  <div class="cmp-card" @dragstart="dragBegin">
    <img class="cmp-bkg" :src="require('@/assets/imgs/card-' + card.type + '.png')"/>
    <div class="cmp-body v-flex">
      <p class="cmp-card-name">{{card.name}}</p>
      <p class="cmp-card-image flex-fill"></p>
      <p class="cmp-card-text">{{card.text}}</p>
      <a v-if="card.suit" class="cmp-card-suit">
        <sign :s="card.suit" />
      </a>
      <a v-if="card.value" class="cmp-card-number">
        <sign :s="card.value" />
      </a>
    </div>
    <a class="cmp-handle"></a>
  </div>
</template>

<!-- this is a comment -->
<!-- hellow -->

<script>

import { mapGetters } from 'vuex'
import Sign from './Sign'

export default {
  props: ['data'],
  computed: {
    ...mapGetters('game', ['card_info']),
    card() {
      return this.card_info(this.data)
    }
  },
  methods: {
    dragBegin(e) {
      e.preventDefault();
      this.$emit('card-drag-begin', {position: this.getPosition(), offset: {x: e.clientX, y: e.clientY}})
    },
    getPosition() {
      let r = this.$el.getElementsByClassName('cmp-handle')[0].getBoundingClientRect()

      return {left: r.x, bottom: r.y}
    }
  },
  components: {
    Sign
  }
}
</script>

<style scoped>

.cmp-card {
  display: inline-block;
  position: relative;
  width: 206px;
  height: 294px;
}

.cmp-bkg {
  filter: drop-shadow(1px 1px 8px rgba(0,0,0, 0.25));
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
}

.cmp-card-name {
  text-align: center;
  font-family: 'Western';
  font-size: 18px;
}

.cmp-card-text {
  font-family: 'Western';
  font-size: 11px;
  line-height: 14px;
  color: #565656;
}

.cmp-card.reversed .cmp-card-text {
  transform: rotate(180deg);
}

.cmp-card-suit {
  position: absolute;
  bottom: 14px;
  left: 18px;
}

.cmp-card-number {
  position: absolute;
  bottom: 4px;
  left: 8px;
}

.cmp-body {
  height: 100%;
  box-sizing: border-box;
  padding: 26px 24px;
  position: relative;
  pointer-events: none;
}

.cmp-handle {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 0;
}

</style>