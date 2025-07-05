<template>
  <div class="py-6 w-full max-w-md mx-auto">
    <div class="bg-white rounded-lg shadow-lg overflow-hidden p-8">
      <h2 class="text-2xl font-semibold text-gray-700 text-center mb-2">AstroBot</h2>
      <p class="text-xl text-gray-600 text-center mb-6">Welcome back!</p>

      <div class="space-y-4">
        <div>
          <label class="block text-gray-700 text-sm font-bold mb-1">Email Address</label>
          <input v-model="email" type="email" required
            class="bg-gray-200 text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 w-full appearance-none" />
        </div>

        <div>
          <label class="block text-gray-700 text-sm font-bold mb-1">Password</label>
          <input v-model="password" type="password" required
            class="bg-gray-200 text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 w-full appearance-none" />
        </div>

        <button @click="login"
          class="bg-gray-700 text-white font-bold py-2 px-4 w-full rounded hover:bg-gray-600 transition">
          Login
        </button>
      </div>

      <div class="mt-4 flex items-center justify-between">
        <span class="border-b w-1/5 md:w-1/4"></span>
        <button @click="$emit('toggle')"
          class="text-xs text-gray-500 uppercase">or sign up</button>
        <span class="border-b w-1/5 md:w-1/4"></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const email = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
  try {
    const response = await api.post('/login', {
      email: email.value,
      password: password.value,
    })
    alert('Login successful!')
    console.log('Token:', response.data.access_token)

    // ✅ Example redirect to /dashboard after login
    router.push('/dashboard')
  } catch (error) {
    console.error('Login failed:', error.response?.data || error.message)
    alert('Login failed: ' + (error.response?.data.detail || error.message))
  }
}
</script>
