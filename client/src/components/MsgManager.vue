<template>
  <transition-group class="cmp-msg-manager" tag="div" name="comic" appear>
    <div @click="message.remove()" v-for="message in msgs" :key="message.id" class="modal">
      <img :src="require('@/assets/imgs/comics/' + imgs[message.type])"/>
      <div class="modal-body v-flex center" style="padding: 0 64px;">{{message.text}}</div>
    </div>
  </transition-group>
</template>

<script>
export default {
  data: function () {
    return {
      imgs: {
        'warning': 'comic_warning.png',
        'info': 'comic_default.png'
      }
    }
  },
  computed: {
    msgs: function() {
      return this.$store.state.msgmanager.msgs
    }
  }
}
</script>

<style scoped>

.cmp-msg-manager {
  position: fixed;
  top: 0;
  right: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column-reverse;
  align-items: flex-end;
  pointer-events: none;
  font-family: 'Western';
  font-size: 18px;
}

.modal {
  display: inline-block;
  pointer-events: all;
  z-index: 1;
}

.comic-move {
  transition: .3s;
}

.comic-enter-active {
  transition: transform .3s cubic-bezier(.17,.67,.16,1.4);
}
.comic-enter {
  transform: translate(100%, 100%) scale(0);
}

.comic-leave-active {
  z-index: 0 !important;
  transition: transform 1s ease;
  position: absolute;
}
.comic-leave-to {
  transform: translate(100%, 0) scale(0);
}

</style>