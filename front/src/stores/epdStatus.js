import { defineStore } from 'pinia'
import { useUiStatusStore } from '@/stores/uiStatus'

const HOST = `${window.location.protocol}//${window.location.hostname}`
const STATUS_ENPOINT = `${HOST}:8888/api/status`
const CURRENT_DISPLAY_ENPOINT = `${HOST}:8888/api/current_display`

export const useEpdStatusStore = defineStore({
  id: 'epdStatus',
  state: () => ({
    currentView: null,
    epdBusy: null,
    totalViews: null,
    currentImage: null,
    timestamp: null,
  }),
  actions: {
    async fetchStatus() {
      const uiStatusStore = useUiStatusStore()

      if ( !uiStatusStore.fetchingStatus ) {
        uiStatusStore.$patch({
          fetchingStatus: true
        })
        fetch( STATUS_ENPOINT )
        .then( response => {
          return response.json()
        })
        .then( data => {
          if ( this.timestamp !== data.timestamp ) {
            uiStatusStore.$patch({
              loadingImage: true
            })
            this.fetchCurrentImage()
          }
          this.timestamp = data.timestamp
          this.epdBusy = data.epd_busy
          this.totalViews = data.total_views
          this.currentView = data.current_view

          let currentDate = new Date().toLocaleString()
          uiStatusStore.$patch({
            lastSuccessfulCheck: currentDate,
            failedRequestsCount: 0
          })
        })
        .catch(error => {
          uiStatusStore.$patch({
            errorAlert: true,
            successAlert: false,
            warningAlert: false,
            failedRequestsCount: uiStatusStore.failedRequestsCount + 1
          })
          console.error( 'Error while fetching the status from API:', error )
        })
        .finally(() => {
          uiStatusStore.$patch({
            fetchingStatus: false
          })
        })
      }
    },
    async fetchCurrentImage() {
      const uiStatusStore = useUiStatusStore()

      fetch( CURRENT_DISPLAY_ENPOINT )
      .then( response => {
        return response
      })
      .then( response => response.blob() )
      .then( blob => {
          this.currentImage = URL.createObjectURL(blob)
          uiStatusStore.$patch({
            loadingImage: false
          })
      })
      .catch( error => {
        uiStatusStore.$patch({
          errorAlert: true,
          successAlert: false,
          warningAlert: false
        })
        console.error( 'Error while loading an image:', error );
      })
    },
  },
})
