import { defineStore } from 'pinia'

export const useStatusStore = defineStore({
  id: 'status',
  state: () => ({
    currentView: null,
    epdBusy: null,
    totalViews: null,
    loadingImage: false,
    currentImage: null,
    timestamp: null,
    successAlert: false,
    warningAlert: false,
    errorAlert: false,
    failedRequestsCount: 0,
    lastSuccessfulCheck: null
  }),
  actions: {
    async fetchStatus() {
      fetch('http://localhost:8888/api/status')
      .then(response => {
        return response.json()
      })
      .then(data => {
        if (this.timestamp !== data.timestamp) {
          this.loadingImage = true
          this.fetchCurrentImage()
        }
        this.timestamp = data.timestamp
        this.epdBusy = data.epd_busy
        this.totalViews = data.total_views
        this.currentView = data.current_view
        let currentDate = new Date().toLocaleString()
        this.lastSuccessfulCheck = currentDate
        this.failedRequestsCount = 0
      })
      .catch(error => {
        this.failedRequestsCount++
        this.resetAlerts()
        this.errorAlert = true
        console.error('Error while loading a status:', error)
      })
    },
    fetchCurrentImage() {
      fetch('http://localhost:8888/api/current_display')
      .then(response => {
        return response
      })
      .then(response => response.blob())
      .then(blob => {
          this.currentImage = URL.createObjectURL(blob)
          this.loadingImage = false
      })
      .catch(error => {
        this.resetAlerts()
        this.errorAlert = true
        console.error('Error while loading an image:', error);
      })
    },
    resetAlerts () {
      this.successAlert = false
      this.warningAlert = false
      this.errorAlert = false
    }
  },
})
