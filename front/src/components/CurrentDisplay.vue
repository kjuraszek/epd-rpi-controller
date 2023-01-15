<template>
  <v-img
    v-if="currentImage"
    :class="currentImageClass" 
    :src="currentImage"
  />
  <p v-else>
    Unable to load an image, check if API and EPD are working.
  </p>
  <CurrentDisplayInfo />
</template>

<script>
  import CurrentDisplayInfo from '@/components/CurrentDisplayInfo.vue'
  import { useEpdStatusStore } from '@/stores/epdStatus'
  import { useUiStatusStore } from '@/stores/uiStatus'
  import { mapState } from 'pinia'

  export default {
    components: {
      CurrentDisplayInfo
    },
    computed: {
      ...mapState(useEpdStatusStore, ['currentImage']),
      ...mapState(useUiStatusStore, ['loadingImage']),
      currentImageClass () {
        return this.loadingImage ? 'current-image img-loading-shadow' : 'current-image img-no-shadow'
      }
    },
  }
</script>

<style>
.current-image.img-no-shadow{
  box-shadow: None;
  transition: all 1.5s;
}
.current-image.img-loading-shadow{
  box-shadow: 0px 0px 30px #009688;
  opacity:0.8;
}

</style>