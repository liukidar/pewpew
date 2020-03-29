<template>
  <div class="cmp-hand">
    <div class="cmp-cards-wrapper">
      <card @card-drag-begin="(e) => { pickCard(index, e) }" v-for="(el, index) in you.hand" :key="el.pid" :data="el"
        :style="{transform: `translateX(-50%) rotateZ(${angle(index)}rad)`, transformOrigin: `50% calc(100% + ${radius}px)`}">
      </card>
    </div>
    <div v-if="viewed_player != you" class="cmp-opponent-hand">
      <card class="reversed" :data="viewed_player.character" />
      <interaction v-for="el in viewed_player.hand" :key="el.pid" to="top" :actions="[{
        text: 'discard',
        action: '_moveCard',
        data: {
          from: 'hand/' + viewed_player.name,
          to: 'discards',
          pid: el.pid
        }
      },{
        text: 'pick',
        action: '_moveCard',
        data: {
          from: 'hand/' + viewed_player.name,
          to: 'hand/' + you.name,
          pid: el.pid
        }
      }]">
        <img :src="require('@/assets/imgs/card-background.png')">
      </interaction>
    </div>
  </div>
</template>

<script>

import { mapGetters, mapActions } from 'vuex'
import Interaction from './Interaction'

import Card from './Card'
export default {
  data: function() {
    return {
      floatings: [],
      picked: null,
      radius: 800,
      aperture: Math.PI / 4
    }
  },
  computed: {
    ...mapGetters('game/match', ['you', 'viewed_player']),
    angle() {
      return (i) => this.computeAngle(i)
    }
  },
  methods: {
    ...mapActions('game/match', ['_playCard', '_moveCard']),
    computeAngle(i) {
      let angle = Math.min(this.aperture / this.you.hand.length, 0.16)

      return (i - this.you.hand.length / 2) * angle + angle / 2
    },
    pickCard(_index, _drag) {
      let wrapper = this.$el.children[0]
      wrapper.classList.add('picking')
      let r = wrapper.getBoundingClientRect()
      this.picked = { index: _index, card: this.you.hand[_index], el: this.$el.children[0].children[_index],
        offset: {b: r.bottom - _drag.position.bottom + _drag.offset.y, l: r.left - _drag.position.left + _drag.offset.x} }
      
      this.picked.el.classList.add('floating')
      this.picked.el.style.bottom = r.bottom - _drag.position.bottom + 'px'
      this.picked.el.style.left = - r.left + _drag.position.left + 'px'
      window.addEventListener('mousemove', this.moveCard)
      window.addEventListener('mouseup', this.dropCard)
    },
    moveCard(e) {
      this.$nextTick(() => {
        let angle = Math.atan((e.clientX - this.picked.offset.l) / (this.picked.offset.b + this.radius - e.clientY))
        if (this.picked.index < this.you.hand.length - 1 && angle > this.computeAngle(this.picked.index + 1)) {
          let tmp = this.you.hand[this.picked.index + 1]
          this.you.hand.splice(this.picked.index, 2, tmp, this.picked.card)
          this.picked.index++
        }
        /*else if (this.picked.index > 0 && angle < this.computeAngle(this.picked.index - 1)) {
          let tmp = this.you.hand[this.picked.index - 1]
          this.you.hand.splice(this.picked.index - 1, 2, this.picked.card, tmp)
          this.picked.index--
        }*/
      })
      this.picked.el.style.bottom = this.picked.offset.b - e.clientY + 'px'
      this.picked.el.style.left = e.clientX - this.picked.offset.l + 'px'
    },
    dropCard() {
      let wrapper = this.$el.children[0]
      wrapper.classList.remove('picking')
      let b = this.picked.el.style.bottom
      let l = this.picked.el.style.left
      
      if (parseInt(b) > window.innerHeight - 260 && this.viewed_player != this.you) {
        this._moveCard({ from: 'hand/' + this.you.name, to: 'hand/' + this.viewed_player.name, hid: this.picked.card.hid })
      } else if (parseInt(l) >= window.innerWidth / 2 - 346) {
        this._moveCard({ from: 'hand/' + this.you.name, to: 'discards', hid: this.picked.card.hid })
      } else if (parseInt(b) > 100 && parseInt(b) < window.innerHeight - 260 && this.you == this.viewed_player) {
        this.picked.card.bottom = b
        this.picked.card.left = l
        this._moveCard({ from: 'hand/' + this.you.name, to: 'board/' + this.you.name, hid: this.picked.card.hid, 'card-bottom': b, 'card-left': l})
      } else {
        this.picked.el.classList.remove('floating')
        this.picked.el.style.bottom = ''
        this.picked.el.style.left = ''
      }
      this.picked = null
      //this.floatings.push(this.picked.card)
      //this.cards.splice(this.picked.index, 1)
      window.removeEventListener('mousemove', this.moveCard)
      window.removeEventListener('mouseup', this.dropCard)
    }
  },
  components: {
    Card, Interaction
  }
}
</script>

<style scoped>

.cmp-opponent-hand {
  position: absolute;
  bottom: calc(100vh - 80px);
  left: 0;
  width: 100vw;
  height: 80px;
  transform: rotate(180deg);
}

.cmp-opponent-hand img {
  display: inline-block;
  width: 206px;
  filter: drop-shadow(-1px 5px 10px #000);
  margin: 0 -32px;
}

.cmp-opponent-hand > .cmp-card {
  position: absolute;
  left: 32px;
  top: 0px;
  transition: all .5s;
}

.cmp-opponent-hand:hover > .cmp-card {
  left: 256px;
  top: -248px;
}

.cmp-hand {
  width: 100%;
  position: absolute;
  bottom: 0;
  left: 0;
  height: 30%;
}
.cmp-cards-wrapper {
  position: absolute;
  bottom: -200px;
  left: 50%;
  margin: auto;
  transition: bottom .5s;
}
.cmp-board {
  position: absolute;
  bottom: 0px;
  left: 50%;
}
.cmp-hand:hover > .cmp-cards-wrapper {
  bottom: -80px;
}
.cmp-cards-wrapper.picking {
  bottom: 0 !important;
}
.cmp-cards-wrapper.picking > .cmp-card:not(.floating) {
  bottom: -200px !important;
}

.cmp-card {
  position: absolute;
  bottom: 0;
  left: 0;
  transition: bottom .25s, transform .5s, left .25s;
}
.cmp-card.floating {
  filter: drop-shadow(0px 5px 20px rgba(0,0,0, 0.75));
  transform-origin: 50% 100% !important;
  transform: translateX(-50%) rotateZ(0) !important;
  transition: transform .5s !important;
  z-index: 1;
}
.cmp-cards-wrapper:not(.picking) > .cmp-card:hover {
  bottom: 80px;
  transition: bottom .4s, left .4s, transform .5s;
}

</style>