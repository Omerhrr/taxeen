<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Authenticated Layout -->
    <div v-if="authStore.isAuthenticated" class="flex">
      <!-- Sidebar -->
      <Sidebar />
      
      <!-- Main Content -->
      <div class="flex-1 lg:ml-64">
        <Header />
        <main class="p-6">
          <router-view />
        </main>
      </div>
    </div>
    
    <!-- Guest Layout -->
    <div v-else>
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import Sidebar from '@/components/layout/Sidebar.vue'
import Header from '@/components/layout/Header.vue'

const authStore = useAuthStore()
</script>
