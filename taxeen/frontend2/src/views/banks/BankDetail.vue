<template>
  <div>
    <div class="mb-6">
      <router-link to="/banks" class="text-primary-600 hover:text-primary-700 text-sm font-medium">← Back to Banks</router-link>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mt-2">{{ bank?.bank_name || 'Bank Account' }}</h1>
    </div>
    
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="p-6">
        <div class="flex items-center mb-6">
          <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-teal-600 rounded-lg flex items-center justify-center mr-4">
            <span class="text-white font-bold text-xl">{{ bank?.bank_name?.substring(0, 2) }}</span>
          </div>
          <div>
            <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ bank?.bank_name }}</h2>
            <p class="text-gray-500 dark:text-gray-400">{{ bank?.account_number }}</p>
          </div>
        </div>
        
        <div class="grid grid-cols-2 gap-6 mb-6">
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Account Name</p>
            <p class="font-medium text-gray-900 dark:text-white">{{ bank?.account_name }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Account Type</p>
            <p class="font-medium text-gray-900 dark:text-white">{{ bank?.account_type }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Current Balance</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ formatCurrency(bank?.current_balance) }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Status</p>
            <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
              {{ bank?.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Transactions -->
    <div class="mt-6 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="p-4 border-b border-gray-200 dark:border-gray-700">
        <h3 class="font-semibold text-gray-900 dark:text-white">Recent Transactions</h3>
      </div>
      <div class="p-4 text-center text-gray-500 dark:text-gray-400">
        Upload a bank statement to see transactions
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const bank = ref(null)

onMounted(async () => {
  // Mock bank data
  bank.value = {
    id: route.params.id,
    bank_name: 'Guaranty Trust Bank',
    account_number: '****1234',
    account_name: 'JOHN DOE',
    account_type: 'Savings',
    current_balance: 2450000,
    is_active: true
  }
})

function formatCurrency(value) {
  return new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN' }).format(value || 0)
}
</script>
