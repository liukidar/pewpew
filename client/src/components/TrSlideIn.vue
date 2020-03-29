<template>
  <transition-group tag="div" class="tr-slide-in"
    appear
    v-bind:css="false"
    v-on:before-enter="beforeEnter"
    v-on:enter="enter"
    v-on:leave="leave"
    >
    <slot></slot>
  </transition-group>
</template>

<script>
export default {
  props: {
    duration: {
      default: '1s'
    },
    stagger: {
      default: 0
    },
    settings: {
      default: function() {
        return {
          from: '-100%, 0%'
        }
      }
    }
  },
  data: function() {
    return {
      status: []
    }
  },
  methods: {
    beforeEnter: function(el) {
      el.targetTransition = 'transform'
      el.style.transition = this.duration
      if (el.dataset.from) {
        el.style.transform = 'translate(' + el.dataset.from + ')'
      } else {
        el.style.transform = 'translate(' + this.settings.from + ')'
      }
      el.end = function(e) {
        if (e.propertyName === el.targetTransition && e.target === el) {
          this.done()
          this.removeEventListener('transitionend', el.end)
        }
      }
    },
    enter: function(el, done) {
      el.style.transition = this.duration
      let delay = el.dataset.index * this.stagger
      el.done = done
      window.requestAnimationFrame(() => {
        setTimeout(() => {
          el.style.transform = 'translate(0, 0)'
          el.addEventListener('transitionend', el.end, false)
        }, delay)
      })
    },
    leave: function(el, done) {
      el.style.transition = this.duration
      let delay = el.dataset.index * this.stagger
      el.done = done
      window.requestAnimationFrame(() => {
        setTimeout(() => {
          if (el.dataset.from) {
            el.style.transform = 'translate(' + el.dataset.from + ')'
          } else {
            el.style.transform = 'translate(' + this.settings.from + ')'
          }
          el.addEventListener('transitionend', el.end, false)
        }, delay)
      })
    }
  }
}
</script>
