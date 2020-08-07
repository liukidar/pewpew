<template>
  <div class="cmp-sign">
    <img :src="require('@/assets/imgs/signs/' + s + '.png')" />
  </div>
</template>

<script>
export default {
  props: ['s']
}
</script>

<style scoped>

.cmp-sign {
  display: inline-block;
}

img {
  width: 100%;
}

</style>