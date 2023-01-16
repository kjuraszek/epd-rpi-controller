<template>
  <div class="text-center">
    <v-snackbar
      v-model="successAlert"
      :timeout="timeout"
      variant="tonal"
      class="pa-0"
    >
      <v-alert
        width="100%"
        type="success"
      >
        View change has been triggered.
      </v-alert>
    </v-snackbar>

    <v-snackbar
      v-model="warningAlert"
      :timeout="timeout"
      variant="tonal"
      class="pa-0"
    >
      <v-alert
        width="100%"
        type="warning"
      >
        Warning - EPD is busy at this moment, wait a while and retry your action.
      </v-alert>
    </v-snackbar>

    <v-snackbar
      v-model="errorAlert"
      :timeout="timeout"
      variant="tonal"
      class="pa-0"
    >
      <v-alert
        width="100%"
        type="error"
      >
        Action failed - unable to connect to an API.
        <span v-if="lastSuccessfulCheck"> Last successful check: {{ lastSuccessfulCheck }}</span>
      </v-alert>
    </v-snackbar>
  </div>
</template>

<script>
  import { useUiStatusStore } from '@/stores/uiStatus'
  import { mapWritableState, mapActions } from 'pinia'

  export default {
    data: () => ({
      timeout: 3000,
    }),
    computed: {
      ...mapWritableState(useUiStatusStore, ['successAlert', 'warningAlert', 'errorAlert', 'lastSuccessfulCheck'])
    },
    methods: {
      ...mapActions(useUiStatusStore, ['resetAlerts']),
    }
  }
</script>

<style>
.v-snackbar__wrapper .v-snackbar__content {
  padding: 0
}
</style>
