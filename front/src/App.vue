<template>
  <v-app>
    <v-app-bar
      app
      class="bg-teal"
      light
      flat
    >
    </v-app-bar>

    <v-main>
      <Main />
    </v-main>
    
    <Footer />

  </v-app>

</template>

<script>
  import Main from '@/components/Main.vue'
  import Footer from '@/components/Footer.vue'
  import { useUiStatusStore } from '@/stores/uiStatus'
  import { useEpdStatusStore } from '@/stores/epdStatus'
  import { mapState, mapActions } from 'pinia'

  export default {
  name: 'App',
  components: {
    Main, Footer
  },
  computed: {
    ...mapState( useUiStatusStore, ['failedRequestsCount'] )
  },
  data () {
    return {
      interval: null
    }
  },
  mounted() {
    this.startInterval()
  },
  methods: {
    ...mapActions( useEpdStatusStore, ["fetchStatus"] ),
    startInterval () {
      clearInterval(this.interval)
      this.interval = setInterval(() => {
        this.fetchStatus()
      }, 1000)
    }
  },
  watch: {
    failedRequestsCount (newValue, oldValue) {
      if (newValue > 50) {
        clearInterval( this.interval )
      }
    }
  },
  beforeDestroy () {
    clearInterval( this.interval )
  }
}

</script>
