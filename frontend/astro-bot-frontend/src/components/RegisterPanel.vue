<template>
  <div class="py-6 w-full max-w-md mx-auto">
    <div class="bg-white rounded-lg shadow-lg overflow-hidden p-8">
      <h2 class="text-2xl font-semibold text-gray-700 text-center mb-2">AstroBot</h2>
      <p class="text-xl text-gray-600 text-center mb-6">Create an Account</p>

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

        <div>
          <label class="block text-gray-700 text-sm font-bold mb-1">Username</label>
          <input v-model="username" type="text" required
            class="bg-gray-200 text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 w-full appearance-none" />
        </div>

        <div>
          <label class="block text-gray-700 text-sm font-bold mb-1">Profile Picture (optional)</label>
          <input type="file" @change="handleFileUpload"
            class="bg-gray-200 text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 w-full appearance-none" />
        </div>

        <button @click="register"
          class="bg-gray-700 text-white font-bold py-2 px-4 w-full rounded hover:bg-gray-600 transition">
          Register
        </button>
      </div>

      <div class="mt-4 flex items-center justify-between">
        <span class="border-b w-1/5 md:w-1/4"></span>
        <button @click="$emit('toggle')"
          class="text-xs text-gray-500 uppercase">or login</button>
        <span class="border-b w-1/5 md:w-1/4"></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'
import { ref, defineEmits } from 'vue'

const emit = defineEmits(['registered'])  // register the custom event


const email = ref('')
const password = ref('')
const username = ref('')
const profilePicture = ref(null)

const handleFileUpload = (event) => {
  profilePicture.value = event.target.files[0]
}

const register = async () => {
  const formData = new FormData()
  formData.append('email', email.value)
  formData.append('password', password.value)
  formData.append('username', username.value)
  if (profilePicture.value) formData.append('profile_picture', profilePicture.value)

  try {
    const response = await api.post('/register', formData)
    alert('Registration successful!')
    console.log('Registered user:', response.data)
  } catch (error) {
    console.error('Registration failed:', error.response?.data || error.message)
    alert('Registration failed: ' + (error.response?.data.detail || error.message))
  }
}
</script>
