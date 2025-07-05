<template>
  <v-app>
    <v-main class="flex justify-center items-center min-h-screen bg-gray-100">
      <transition name="fade" mode="out-in">
        <register-panel 
          v-if="isRegister" 
          key="register"
          @toggle="isRegister = false" 
          @registered="isRegister = false" 
        />
        <login-panel 
          v-else 
          key="login"
          @toggle="isRegister = true" 
        />
      </transition>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import RegisterPanel from './components/RegisterPanel.vue'
import LoginPanel from './components/LoginPanel.vue'

const isRegister = ref(true)
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
