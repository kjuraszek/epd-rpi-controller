<template>
  <div v-if="currentView !== null && totalViews !== null">
    <v-progress-linear
      :model-value="currentViewProportional"
      color="teal"
      rounded
    />
    
    <p v-if="epdBusy">
      (EPD is switching)
    </p>
    <p v-else>
&nbsp;
    </p>

    <p class="text-h5 my-3 font-weight-regular">
      <em>View {{ currentView + 1 }} of {{ totalViews }}</em>
    </p>
  </div>
</template>

<script>
  import { useEpdStatusStore } from '@/stores/epdStatus'
  import { mapState } from 'pinia'

  /**
  * Component displays the data about views progress and the current state of the EPD.
  */
  export default {
    computed: {
      ...mapState(useEpdStatusStore, ['currentView', 'totalViews', 'epdBusy']),
      currentViewProportional () {
        return Math.round((this.currentView + 1) / this.totalViews * 100)
      }
    }
  }
</script>
