<template>
  <v-app>
    <v-app-bar
      app
      class="bg-teal"
      light
      flat
    />

    <v-main>
      <AppMain />
      <AppAlerts />
    </v-main>
    
    <AppFooter />
  </v-app>
</template>

<script>
  import AppAlerts from '@/components/AppAlerts.vue'
  import AppMain from '@/components/AppMain.vue'
  import AppFooter from '@/components/AppFooter.vue'
  import { useUiStatusStore } from '@/stores/uiStatus'
  import { useEpdStatusStore } from '@/stores/epdStatus'
  import { mapState, mapActions } from 'pinia'

  export default {
  name: 'App',
  components: {
    AppMain, AppFooter, AppAlerts
  },
  data () {
    return {
      interval: null
    }
  },
  computed: {
    ...mapState( useUiStatusStore, ['failedRequestsCount'] )
  },
  watch: {
    // eslint-disable-next-line no-unused-vars
    failedRequestsCount (newValue, oldValue) {
      if (newValue > 50) {
        clearInterval( this.interval )
      }
    }
  },
  mounted() {
    this.startInterval()
  },
  beforeUnmount () {
    clearInterval( this.interval )
  },
  methods: {
    ...mapActions( useEpdStatusStore, ["fetchStatus"] ),
    startInterval () {
      clearInterval(this.interval)
      this.interval = setInterval(() => {
        this.fetchStatus()
      }, 600)
    }
  },
}

</script>
