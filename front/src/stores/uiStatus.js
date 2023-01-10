import { defineStore } from 'pinia'

export const useUiStatusStore = defineStore({
  id: 'uiStatus',
  state: () => ({
    loadingImage: false,
    successAlert: false,
    warningAlert: false,
    errorAlert: false,
    failedRequestsCount: 0,
    lastSuccessfulCheck: null,
    fetchingStatus: false
  }),
  actions: {
    resetAlerts () {
      this.successAlert = false
      this.warningAlert = false
      this.errorAlert = false
    }
  },
})
