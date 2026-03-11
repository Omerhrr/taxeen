<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-50 to-teal-100 dark:from-gray-900 dark:to-gray-800 py-12 px-4">
    <div class="max-w-md w-full">
      <!-- Logo -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-primary-600 dark:text-primary-500">Taxeen</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">Nigerian Personal Tax Intelligence</p>
      </div>
      
      <!-- Login Card -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Welcome Back</h2>
        
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
            <input 
              v-model="form.email"
              type="email"
              required
              class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="you@example.com"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Password</label>
            <input 
              v-model="form.password"
              type="password"
              required
              class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="••••••••"
            />
          </div>
          
          <div v-if="error" class="p-3 bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 rounded-lg text-sm">
            {{ error }}
          </div>
          
          <button 
            type="submit"
            :disabled="loading"
            class="w-full py-3 px-4 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>
        
        <div class="mt-6 text-center">
          <p class="text-gray-600 dark:text-gray-400">
            Don't have an account?
            <router-link to="/register" class="text-primary-600 hover:text-primary-700 dark:text-primary-500 font-medium">
              Sign up
            </router-link>
          </p>
        </div>
        
        <!-- Demo -->
        <div class="mt-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <p class="text-sm text-gray-600 dark:text-gray-400 text-center">
            Demo: <strong>demo@taxeen.ng</strong> / <strong>demo123</strong>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const error = ref('')

const form = reactive({
  email: '',
  password: ''
})

async function handleLogin() {
  loading.value = true
  error.value = ''
  
  const result = await authStore.login(form.email, form.password)
  
  if (result.success) {
    router.push('/')
  } else {
    error.value = result.message
    
    // Demo mode fallback
    if (form.email === 'demo@taxeen.ng' && form.password === 'demo123') {
      authStore.user = {
        id: 1,
        email: 'demo@taxeen.ng',
        first_name: 'Demo',
        last_name: 'User',
        is_admin: false
      }
      authStore.token = 'demo-token'
      localStorage.setItem('token', 'demo-token')
      router.push('/')
    }
  }
  
  loading.value = false
}
</script>
