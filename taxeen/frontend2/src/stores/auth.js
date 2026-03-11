import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  
  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin || false)
  
  // Actions
  async function login(email, password) {
    try {
      const response = await api.post('/auth/login', { email, password })
      token.value = response.data.access_token
      user.value = response.data.user
      localStorage.setItem('token', token.value)
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Login failed' 
      }
    }
  }
  
  async function register(data) {
    try {
      const response = await api.post('/auth/register', data)
      token.value = response.data.access_token
      user.value = response.data.user
      localStorage.setItem('token', token.value)
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Registration failed' 
      }
    }
  }
  
  async function fetchUser() {
    if (!token.value) return
    
    try {
      const response = await api.get('/auth/me')
      user.value = response.data
    } catch (error) {
      logout()
    }
  }
  
  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }
  
  // Initialize
  if (token.value) {
    fetchUser()
  }
  
  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    login,
    register,
    fetchUser,
    logout
  }
})
