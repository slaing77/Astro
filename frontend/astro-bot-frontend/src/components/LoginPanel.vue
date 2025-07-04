<template>
  <v-card class="pa-6" max-width="500" elevation="8">
    <v-card-title class="text-h5">Login</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="login">
        <v-text-field v-model="email" label="Email" type="email" required />
        <v-text-field v-model="password" label="Password" type="password" required />
        <v-btn type="submit" color="primary" block>Login</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')

const login = () => {
  fetch('http://localhost:8000/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ email: email.value, password: password.value }),
  })
    .then(async (res) => {
      const data = await res.json()
      if (res.ok) {
        alert('Login successful!')
        // Save token or session info here if needed
      } else {
        alert('Login failed: ' + data.detail)
      }
    })
    .catch((err) => console.error('Login error', err))
}
</script>
