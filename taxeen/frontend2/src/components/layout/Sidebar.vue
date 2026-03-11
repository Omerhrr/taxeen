<template>
  <aside 
    class="fixed left-0 top-0 z-40 h-screen w-64 bg-white border-r border-gray-200 dark:bg-gray-800 dark:border-gray-700 transition-transform"
    :class="{ '-translate-x-full': !isOpen, 'translate-x-0': isOpen }"
  >
    <div class="h-full px-3 py-4 overflow-y-auto">
      <!-- Logo -->
      <router-link to="/" class="flex items-center ps-2.5 mb-5">
        <span class="self-center text-xl font-bold text-primary-600 dark:text-primary-500">Taxeen</span>
      </router-link>
      
      <!-- Navigation -->
      <nav class="space-y-1">
        <router-link 
          to="/" 
          class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
          active-class="bg-gray-100 dark:bg-gray-700"
        >
          <HomeIcon class="w-5 h-5" />
          <span class="ms-3">Dashboard</span>
        </router-link>
        
        <!-- Banks Section -->
        <div>
          <button 
            @click="banksOpen = !banksOpen"
            class="flex items-center w-full p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <BuildingIcon class="w-5 h-5" />
            <span class="ms-3 flex-1 text-left">Banks</span>
            <ChevronIcon :class="{ 'rotate-180': banksOpen }" class="w-4 h-4 transition-transform" />
          </button>
          <ul v-show="banksOpen" class="py-2 space-y-1">
            <li>
              <router-link 
                to="/banks" 
                class="flex items-center p-2 ps-10 text-gray-600 rounded-lg dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
                active-class="bg-gray-100 dark:bg-gray-700"
              >
                All Banks
              </router-link>
            </li>
            <li>
              <router-link 
                to="/banks/add" 
                class="flex items-center p-2 ps-10 text-gray-600 rounded-lg dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
                active-class="bg-gray-100 dark:bg-gray-700"
              >
                Add Bank
              </router-link>
            </li>
          </ul>
        </div>
        
        <router-link 
          to="/transactions" 
          class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
          active-class="bg-gray-100 dark:bg-gray-700"
        >
          <ClipboardIcon class="w-5 h-5" />
          <span class="ms-3">Transactions</span>
        </router-link>
        
        <router-link 
          to="/uploads" 
          class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
          active-class="bg-gray-100 dark:bg-gray-700"
        >
          <UploadIcon class="w-5 h-5" />
          <span class="ms-3">Uploads</span>
        </router-link>
        
        <router-link 
          to="/reports" 
          class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
          active-class="bg-gray-100 dark:bg-gray-700"
        >
          <ChartIcon class="w-5 h-5" />
          <span class="ms-3">Tax Reports</span>
        </router-link>
        
        <router-link 
          to="/settings" 
          class="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
          active-class="bg-gray-100 dark:bg-gray-700"
        >
          <CogIcon class="w-5 h-5" />
          <span class="ms-3">Settings</span>
        </router-link>
      </nav>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  isOpen: { type: Boolean, default: true }
})

const banksOpen = ref(true)

// Icons
const HomeIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>`
}
const BuildingIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>`
}
const ClipboardIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>`
}
const UploadIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>`
}
const ChartIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>`
}
const CogIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>`
}
const ChevronIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>`
}
</script>
