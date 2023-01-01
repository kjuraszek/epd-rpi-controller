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

<script setup>
  import Main from '@/components/Main.vue'
  import Footer from '@/components/Footer.vue'
</script>
