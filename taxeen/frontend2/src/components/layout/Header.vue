<template>
  <header class="sticky top-0 z-30 bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700">
    <div class="px-4 py-3 flex items-center justify-between">
      <!-- Mobile menu button -->
      <button 
        @click="sidebarStore.toggle()"
        class="lg:hidden p-2 text-gray-500 rounded-lg hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
      
      <div class="flex items-center space-x-4">
        <!-- Notifications -->
        <button class="p-2 text-gray-500 rounded-lg hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
          </svg>
        </button>
        
        <!-- User Menu -->
        <div class="relative" ref="userMenuRef">
          <button 
            @click="userMenuOpen = !userMenuOpen"
            class="flex items-center space-x-2"
          >
            <div class="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center text-white font-medium">
              {{ userInitials }}
            </div>
            <span class="hidden md:block text-sm font-medium text-gray-700 dark:text-gray-200">
              {{ authStore.user?.first_name }} {{ authStore.user?.last_name }}
            </span>
          </button>
          
          <div 
            v-show="userMenuOpen"
            class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg dark:bg-gray-700 py-1"
          >
            <router-link 
              to="/settings" 
              class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600"
              @click="userMenuOpen = false"
            >
              Settings
            </router-link>
            <button 
              @click="handleLogout"
              class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100 dark:text-red-400 dark:hover:bg-gray-600"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const userMenuOpen = ref(false)
const userMenuRef = ref(null)

const userInitials = computed(() => {
  const first = authStore.user?.first_name?.[0] || 'U'
  const last = authStore.user?.last_name?.[0] || ''
  return `${first}${last}`
})

// Simple sidebar store
const sidebarStore = {
  isOpen: true,
  toggle() {
    this.isOpen = !this.isOpen
    // Emit event for parent to handle
    window.dispatchEvent(new CustomEvent('sidebar-toggle', { detail: this.isOpen }))
  }
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}

// Close menu on outside click
function handleClickOutside(event) {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    userMenuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
