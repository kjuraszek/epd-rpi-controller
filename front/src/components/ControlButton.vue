<template>
  <v-btn
    color="primary"
    @click="switchView()"
  ><v-icon
    right
    dark
    large
    >
      {{ ACTIONDATA[this.controlAction]['icon'] }}
    </v-icon>
    <v-tooltip
        activator="parent"
        location="bottom"
      >{{ ACTIONDATA[this.controlAction]['label'] }}</v-tooltip>
  </v-btn>
</template>

<script>
  import { useUiStatusStore } from '@/stores/uiStatus'
  import { mapWritableState, mapActions } from 'pinia'

  const ACTIONS = new Set(['next', 'prev']);
  const ACTIONDATA = {
    next: {
      label: 'Next view',
      icon:  'mdi-arrow-right-bold-outline'
    },
    prev: {
      label: 'Previous view',
      icon:  'mdi-arrow-left-bold-outline'
    },
  }
  const HOST = `${window.location.protocol}//${window.location.hostname}`

  export default {
    data () {
      return {
        ACTIONDATA,
        HOST
      }
    },
    computed: {
    ...mapWritableState(useUiStatusStore, ['successAlert', 'warningAlert', 'errorAlert'])
    },
    props: {
      controlAction: String
    },
    methods: {
      switchView () {
        fetch(`${HOST}:8888/api/${this.controlAction}`)
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
    mounted () {
      if (!ACTIONS.has(this.controlAction)) {
        throw new Error(`Unknown action ${this.controlAction} in ControlButton component.`);
      }
    }
  }
</script>
