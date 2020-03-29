<template>
  <button @click="click" @mouseover="mousehover" @mouseleave="mouseleave" class="cmp-img-btn h-flex center">
    <a class="cmp-img" :style="{'margin-right': '-' + offset + 'px'}">
      <img :src="require('@/assets/imgs/icons/' + src + suffix[frame] + '.png')">
    </a>
    <a class="cmp-text">
      <slot></slot>
    </a>
  </button>
</template>

<script>
export default {
  props: {
    src: {
      default: null
    },
    offset: {
      default: 0
    },
    t: {
      default: 100
    }
  },
  data: function () {
    return {
      suffix: ['', '_hover', '_active', '_focus'],
      animation: null,
      frame: 0
    }
  },
  methods: {
    mousehover() {
      if (!this.animation) {
        this.frame = 1
      }
    },
    mouseleave() {
      if (!this.animation) {
        this.frame = 0
      }
    },
    click() {
      if (!this.animation) {
        this.animation = setInterval(() => {
          this.frame++
          if (this.frame == this.suffix.length - 1) {
            this.$emit('click')
          } else if (this.frame == this.suffix.length) {
            clearInterval(this.animation)
            this.frame = 0
            this.animation = null
          }
        }, this.t)
      }
    }
  }
}
</script>

<style scoped>

.cmp-img-btn {
  position: relative;
  display: inline-flex;
  background: none;
  border: none;
  outline: none !important;
  cursor: pointer;
}
.cmp-img-btn.x1_5 {
  transform: scale(1.5);
}

.cmp-text {
  font-family: 'Western';
  letter-spacing: 1px;
  padding-left: 8px;
  font-size: 14px;
  color: #635003;
  text-transform: uppercase;
}
.cmp-img-btn:hover > .cmp-text {
  color: #c49d06
}

</style>