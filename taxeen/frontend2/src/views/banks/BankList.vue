<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Bank Accounts</h1>
        <p class="text-gray-600 dark:text-gray-400">Manage your connected bank accounts</p>
      </div>
      <router-link 
        to="/banks/add"
        class="inline-flex items-center px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
        Add Bank
      </router-link>
    </div>
    
    <div v-if="bankStore.loading" class="text-center py-12">
      <div class="animate-spin w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full mx-auto"></div>
    </div>
    
    <div v-else-if="bankStore.banks.length === 0" class="text-center py-12 bg-white dark:bg-gray-800 rounded-xl">
      <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
      </svg>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No bank accounts yet</h3>
      <p class="text-gray-500 dark:text-gray-400 mb-6">Add your first bank account to start tracking</p>
      <router-link to="/banks/add" class="text-primary-600 hover:text-primary-700 font-medium">Add Bank Account →</router-link>
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="bank in bankStore.banks" 
        :key="bank.id"
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden"
      >
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div class="flex items-center">
              <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-teal-600 rounded-lg flex items-center justify-center mr-4">
                <span class="text-white font-bold">{{ bank.bank_name?.substring(0, 2) }}</span>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 dark:text-white">{{ bank.bank_name }}</h3>
                <p class="text-sm text-gray-500 dark:text-gray-400">{{ bank.account_number }}</p>
              </div>
            </div>
          </div>
          <div class="mt-6">
            <p class="text-sm text-gray-500 dark:text-gray-400">Current Balance</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ formatCurrency(bank.current_balance) }}</p>
          </div>
        </div>
        <div class="px-6 py-4 bg-gray-50 dark:bg-gray-700/50 border-t border-gray-200 dark:border-gray-700">
          <router-link :to="`/banks/${bank.id}`" class="text-primary-600 hover:text-primary-700 font-medium text-sm">
            View Details →
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useBankStore } from '@/stores/banks'

const bankStore = useBankStore()

onMounted(() => {
  bankStore.fetchBanks()
})

function formatCurrency(value) {
  return new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN' }).format(value || 0)
}
</script>
