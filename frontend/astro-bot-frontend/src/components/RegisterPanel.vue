<template>
  <v-card class="pa-6" max-width="500" elevation="8">
    <v-card-title class="text-h5">Create an Account</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="register">
        <v-text-field v-model="email" label="Email" type="email" required />
        <v-text-field v-model="password" label="Password" type="password" required />
        <v-text-field v-model="username" label="Username" required />
        <v-file-input v-model="profilePicture" label="Profile Picture" accept="image/*" prepend-icon="mdi-camera" />
        <v-btn type="submit" color="primary" block>Register</v-btn>
        
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'  // ✅ centralized Axios client with VITE_API_URL

console.log('VITE_API_URL:', import.meta.env.VITE_API_URL)
// ✅ use centralized Axios client for API requests

const email = ref('')
const password = ref('')
const username = ref('')
const profilePicture = ref(null)

const register = async () => {
  const formData = new FormData()
  formData.append('email', email.value)
  formData.append('password', password.value)
  formData.append('username', username.value)
  if (profilePicture.value) {
    formData.append('profile_picture', profilePicture.value)
  }

  try {
    const response = await api.post('/register', formData)  // ✅ USE api, not fetch
    alert('Registration successful!')
    console.log('Registered user:', response.data)
  } catch (error) {
    console.error('Registration failed:', error.response?.data || error.message)
    alert('Registration failed: ' + (error.response?.data.detail || error.message))
  }
}

</script>
