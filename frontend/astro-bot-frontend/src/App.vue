<template>
  <v-app>
    <v-main class="d-flex justify-center align-center" style="min-height: 100vh;">
      <register-panel></register-panel>
      <!-- Or swap with <login-panel></login-panel> for testing -->
    </v-main>
  </v-app>
</template>

<script setup>
import RegisterPanel from './components/RegisterPanel.vue'
import LoginPanel from './components/LoginPanel.vue'
</script>
