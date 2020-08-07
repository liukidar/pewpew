<template>
  <div :style="{width: this.scale * img.w + 'px', height: this.scale * img.h + 'px'}">
    <a :style="{
      'transform': 'scale(' + this.scale + ')',
      'background-image': 'url(' + require('@/assets/imgs/big_pic.png') + ')', 
      'background-position': -img.x + 'px ' + -img.y + 'px', width: img.w + 'px', height: img.h + 'px'
    }" ></a>
  </div>
</template>

<script>

import json from '@/assets/imgs/big_code.json'

export default {
  props: {
    isrc: { // either an image or an animation
      default: ''
    },
    scale: {
      default: 2.0
    },
    animation_speed: {
      default: 1
    }
    /*
    hello_cycles: 10adasdjb
    */
  },
  data: function() {
    return {
      activeFrame: 1,
      i: 0
    }
  },
  computed: {
    img: function() {
      let src = null
      if (json.animations[this.isrc]) {
        // use animation
        src = json.animations[this.isrc].frames[this.activeFrame]
      } else {
        // else it is a static image
        src = this.isrc
      }

      return json.frames[src].frame
    }
  },
  methods: {
    nextFrame: function() {
      if (this.i == 10) {
        this.i = 0
        if (json.animations[this.isrc]) {
          this.activeFrame = (this.activeFrame + 1) % Math.floor(json.animations[this.isrc].frames.length * this.animation_speed)
        }
        // json.animations[this.isrc].frame-duration
      }
      else {
        this.i++
      }
      window.requestAnimationFrame(this.nextFrame)
    }
  },
  mounted: function() {
    this.nextFrame()
  },
  watch: {
    isrc: function() {
      this.nextFrame()
    }
  }
}

</script>

<style scoped>

div {
  display: inline-block;
}
a { 
  display: inline-block;
  transform-origin: 50% 0;
}

</style>
