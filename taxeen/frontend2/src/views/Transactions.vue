<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Transactions</h1>
      <p class="text-gray-600 dark:text-gray-400">View and classify your transactions</p>
    </div>
    
    <!-- Filters -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 mb-6 border border-gray-200 dark:border-gray-700">
      <div class="flex flex-wrap gap-4">
        <select v-model="filters.type" class="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
          <option value="">All Types</option>
          <option value="credit">Credit</option>
          <option value="debit">Debit</option>
        </select>
        <select v-model="filters.category" class="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
          <option value="">All Categories</option>
          <option value="salary">Salary</option>
          <option value="business">Business</option>
          <option value="investment">Investment</option>
          <option value="food">Food & Dining</option>
          <option value="transport">Transport</option>
        </select>
      </div>
    </div>
    
    <!-- Table -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 dark:bg-gray-700/50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Date</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Description</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Category</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Amount</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Balance</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="t in filteredTransactions" :key="t.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50">
              <td class="px-4 py-3 text-sm text-gray-900 dark:text-white">{{ formatDate(t.date) }}</td>
              <td class="px-4 py-3">
                <p class="text-sm text-gray-900 dark:text-white">{{ t.description }}</p>
                <span v-if="t.is_internal" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400">
                  Internal Transfer
                </span>
              </td>
              <td class="px-4 py-3">
                <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
                  {{ t.category }}
                </span>
              </td>
              <td class="px-4 py-3 text-right">
                <span class="text-sm font-medium" :class="t.type === 'credit' ? 'text-green-600' : 'text-red-600'">
                  {{ t.type === 'credit' ? '+' : '-' }}{{ formatCurrency(t.amount) }}
                </span>
              </td>
              <td class="px-4 py-3 text-right text-sm text-gray-600 dark:text-gray-400">
                {{ formatCurrency(t.balance) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'

const filters = reactive({ type: '', category: '' })

const transactions = ref([
  { id: 1, date: '2026-01-15', description: 'Salary Payment - ABC Ltd', type: 'credit', category: 'salary', amount: 850000, balance: 2450000, is_internal: false },
  { id: 2, date: '2026-01-14', description: 'Transfer to GTBank', type: 'debit', category: 'transfer', amount: 50000, balance: 1600000, is_internal: true },
  { id: 3, date: '2026-01-14', description: 'Transfer from Access', type: 'credit', category: 'transfer', amount: 50000, balance: 1650000, is_internal: true },
  { id: 4, date: '2026-01-13', description: 'POS Purchase - Shoprite', type: 'debit', category: 'food', amount: 45000, balance: 1600000, is_internal: false },
  { id: 5, date: '2026-01-12', description: 'Freelance Payment', type: 'credit', category: 'business', amount: 320000, balance: 1645000, is_internal: false },
])

const filteredTransactions = computed(() => {
  return transactions.value.filter(t => {
    if (filters.type && t.type !== filters.type) return false
    if (filters.category && t.category !== filters.category) return false
    return true
  })
})

function formatCurrency(value) {
  return new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN' }).format(value)
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-NG', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>
