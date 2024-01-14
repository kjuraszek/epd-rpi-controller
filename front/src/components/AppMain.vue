<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-1">
        <MainHeadings />
      </v-col>
    </v-row>

    <v-row
      v-if="failedRequestsCount < 50"
      class="text-center"
      justify="center"
    >
      <v-col
        cols="10"
        md="8"
        xl="6"
        class="mb-1 text-center"
        justify="space-between"
      >
        <v-row
          class="text-center"
          justify="center"
        >
          <v-col
            sm="6"
            xl="3"
            class="mb-1 text-center"
            justify="space-between"
          >
            <CurrentDisplay />
          </v-col>
        </v-row>

        <v-row
          class="text-center"
          justify="center"
        >
          <v-col
            sm="4"
            md="2"
            class="mb-1 text-center"
            justify="space-between"
          >
            <ControlButton
              control-action="prev"
            />
          </v-col>
          <v-col
            sm="4"
            md="2"
            class="mb-1 text-center"
            justify="space-between"
          >
            <ControlButton
              control-action="next"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row
      v-else
      class="text-center"
      justify="center"
    >
      <v-col
        cols="12"
        md="8"
        class="mb-1 text-center"
        justify="space-between"
      >
        <v-alert type="error">
          Unable to connect to an API - make sure API and EPD are running and refresh this page.
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import ControlButton from '@/components/ControlButton.vue'
  import CurrentDisplay from '@/components/CurrentDisplay.vue'
  import MainHeadings from '@/components/MainHeadings.vue'
  
  import { useUiStatusStore } from '@/stores/uiStatus'
  import { mapState } from 'pinia'

  /**
  * Application main Component, contains: headings, alerts, display with buttons.
  */
  export default {
    components: {
      ControlButton, CurrentDisplay, MainHeadings
    },
    computed: {
      ...mapState(useUiStatusStore, ['failedRequestsCount'])
    },
  }
</script>
