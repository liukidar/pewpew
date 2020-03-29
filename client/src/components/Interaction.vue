<template>
  <div class="cmp-effect">
    <div class="cmp-body" :class="[to]">
      <div v-for="(el, index) in actions" :key="el.text" :data-index="index">
        <div v-if="el.if || el.if == undefined" class="cmp-action" :style="{transition: '.2s ' + (index * 0.1) + 's'}" @click="execute(el.action, el.data)">
          {{el.text}}
        </div>
      </div>
    </div>
    <slot></slot>
  </div>
</template>

<script>

export default {
  props: {
    actions: {
      default: function() {
        return [
          {
            text: 'NO_ACTION',
            action: 'action',
            data: {},
            if: true
          }
        ]
      }
    },
    to: {
      default: 'left'
    }
  },
  methods: {
    execute(_action, _data) {
      this.$store.dispatch('game/match/' + _action, _data)
    }
  }
}
</script>

<style scoped>

.cmp-effect {
  display: inline-block;
  position: relative;
}

.cmp-body.left {
  position: absolute;
  top: 0;
  right: 100%;
  text-align: right;
}

.cmp-body.top {
  position: absolute;
  left: 0;
  bottom: 100%;
  text-align: left;
}

.cmp-action {
  display: inline-block;
  border-radius: 2px;
  color: #FFF;
  background: #000;
  padding: 8px 16px;
  font-family: 'Western';
  margin-bottom: 16px;
  margin-right: 8px;
  opacity: 0;
  transform: translateX(-50px);
  text-transform: uppercase;
  cursor: pointer;
  pointer-events: all;
}

.cmp-effect:not(:hover) .cmp-body{
  pointer-events: none;
}

.cmp-effect:not(:hover) .cmp-action {
  transition: .5s .2s !important;
}

.cmp-effect:hover .cmp-action {
  opacity: 1;
  transform: translateX(0);
}

input {
  display: inline-block;
  color: #ddd;
  font-size: 14px;
  font-family: 'Western';
  width: auto;
}
</style>