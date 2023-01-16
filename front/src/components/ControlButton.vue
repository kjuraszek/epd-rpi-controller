<template>
  <v-btn
    color="primary"
    @click="switchView()"
  >
    <v-icon
      right
      dark
      large
    >
      {{ ACTIONDATA[controlAction]['icon'] }}
    </v-icon>
    <v-tooltip
      activator="parent"
      location="bottom"
    >
      {{ ACTIONDATA[controlAction]['label'] }}
    </v-tooltip>
  </v-btn>
</template>

<script>
  import { useUiStatusStore } from '@/stores/uiStatus'
  import { mapWritableState, mapActions } from 'pinia'
  import { API } from '@/consts'

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

  export default {
    props: {
      controlAction: {
        type: String,
        required: true
      }
    },
    data () {
      return {
        ACTIONDATA,
        API
      }
    },
    computed: {
    ...mapWritableState(useUiStatusStore, ['successAlert', 'warningAlert', 'errorAlert'])
    },
    mounted () {
      if (!ACTIONS.has(this.controlAction)) {
        throw new Error(`Unknown action ${this.controlAction} in ControlButton component.`);
      }
    },
    methods: {
      switchView () {
        fetch(`${API}/${this.controlAction}`)
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
