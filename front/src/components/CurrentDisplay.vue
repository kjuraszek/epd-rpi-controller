<template>
  <div>
    <v-img
      v-if="currentImage"
      v-touch="{
        left: () => swipeHandler('prev'),
        right: () => swipeHandler('next'),
      }"
      :class="currentImageClass" 
      :src="currentImage"
    />
    <p v-else>
      Unable to load an image, check if API and EPD are working.
    </p>
    <CurrentDisplayInfo />
  </div>
</template>

<script>
  import CurrentDisplayInfo from '@/components/CurrentDisplayInfo.vue'
  import { useEpdStatusStore } from '@/stores/epdStatus'
  import { useUiStatusStore } from '@/stores/uiStatus'
  import { mapWritableState, mapState, mapActions } from 'pinia'
  import { API } from '@/consts'

  /**
  * Component is showing current display with controls and additional data.
  */
  export default {
    components: {
      CurrentDisplayInfo
    },
    computed: {
      ...mapState(useEpdStatusStore, ['currentImage']),
      ...mapWritableState(useUiStatusStore, ['successAlert', 'warningAlert', 'errorAlert', 'loadingImage']),
      
      currentImageClass () {
        return this.loadingImage ? 'current-image img-loading-shadow' : 'current-image img-no-shadow'
      }
    },
    methods: {
      /**
       * Gets called on left or right side of the image. It switches the current view.
       * 
       * @public
       * @param {string} direction direction of swipe
       */
      swipeHandler(direction) {
        fetch(`${API}/${direction}`)
        .then(response => {
          return response
        })
        .then(data => {
           if (data.status >= 500) {
            this.resetAlerts()
            this.errorAlert = true
           } else if (data.status >= 400) {
            this.resetAlerts()
            this.warningAlert = true
           } else {
            this.resetAlerts()
            this.successAlert = true
           }
        })
        .catch(error => {
          this.resetAlerts()
          this.errorAlert = true
          console.error('Error while switching a view:', error);
        })
      },
      ...mapActions(useUiStatusStore, ['resetAlerts']),
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