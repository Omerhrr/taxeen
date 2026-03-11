<template>
  <div>
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
      <p class="text-gray-600 dark:text-gray-400">Welcome back, {{ authStore.user?.first_name || 'User' }}!</p>
    </div>
    
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatsCard 
        title="Total Balance"
        :value="formatCurrency(stats.totalBalance)"
        icon="currency"
        color="emerald"
      />
      <StatsCard 
        title="Total Income"
        :value="formatCurrency(stats.totalIncome)"
        icon="arrow-up"
        color="green"
        :change="+12"
      />
      <StatsCard 
        title="Total Expenses"
        :value="formatCurrency(stats.totalExpenses)"
        icon="arrow-down"
        color="red"
        :change="+5"
      />
      <StatsCard 
        title="Net Savings"
        :value="formatCurrency(stats.netSavings)"
        icon="chart"
        color="blue"
      />
    </div>
    
    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Income vs Expenses</h3>
        <div ref="incomeExpenseChart" class="h-64"></div>
      </div>
      
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Income by Category</h3>
        <div ref="categoryChart" class="h-64"></div>
      </div>
    </div>
    
    <!-- Recent Transactions -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="p-6 border-b border-gray-200 dark:border-gray-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Recent Transactions</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 dark:bg-gray-700/50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Date</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Description</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Amount</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="t in transactions" :key="t.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50">
              <td class="px-4 py-3 text-sm text-gray-900 dark:text-white">{{ formatDate(t.date) }}</td>
              <td class="px-4 py-3 text-sm text-gray-900 dark:text-white">{{ t.description }}</td>
              <td class="px-4 py-3 text-sm text-right font-medium" :class="t.type === 'credit' ? 'text-green-600' : 'text-red-600'">
                {{ t.type === 'credit' ? '+' : '-' }}{{ formatCurrency(t.amount) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import * as echarts from 'echarts'
import StatsCard from '@/components/StatsCard.vue'

const authStore = useAuthStore()
const incomeExpenseChart = ref(null)
const categoryChart = ref(null)

// Mock data
const stats = reactive({
  totalBalance: 3465000,
  totalIncome: 5050000,
  totalExpenses: 3220000,
  netSavings: 1830000
})

const transactions = ref([
  { id: 1, date: '2026-01-15', description: 'Salary Payment - ABC Ltd', type: 'credit', amount: 850000 },
  { id: 2, date: '2026-01-14', description: 'POS Purchase - Shoprite', type: 'debit', amount: 45000 },
  { id: 3, date: '2026-01-13', description: 'Transfer from John', type: 'credit', amount: 150000 },
  { id: 4, date: '2026-01-12', description: 'Airtime Purchase', type: 'debit', amount: 5000 },
  { id: 5, date: '2026-01-11', description: 'Freelance Payment', type: 'credit', amount: 320000 },
])

function formatCurrency(value) {
  return new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN' }).format(value)
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-NG', { day: 'numeric', month: 'short', year: 'numeric' })
}

onMounted(() => {
  // Income vs Expenses Chart
  if (incomeExpenseChart.value) {
    const chart = echarts.init(incomeExpenseChart.value)
    chart.setOption({
      tooltip: { trigger: 'axis' },
      legend: { data: ['Income', 'Expenses'], textStyle: { color: '#6B7280' } },
      xAxis: {
        type: 'category',
        data: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        axisLabel: { color: '#6B7280' }
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: '#6B7280', formatter: v => '₦' + (v/1000000).toFixed(1) + 'M' }
      },
      series: [
        { name: 'Income', type: 'bar', data: [720000, 680000, 850000, 920000, 780000, 1100000], itemStyle: { color: '#10B981' } },
        { name: 'Expenses', type: 'bar', data: [450000, 520000, 480000, 560000, 490000, 720000], itemStyle: { color: '#EF4444' } }
      ]
    })
  }
  
  // Category Chart
  if (categoryChart.value) {
    const chart = echarts.init(categoryChart.value)
    chart.setOption({
      tooltip: { trigger: 'item' },
      legend: { orient: 'vertical', right: '5%', top: 'center', textStyle: { color: '#6B7280' } },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
        label: { show: false },
        data: [
          { value: 6500000, name: 'Salary', itemStyle: { color: '#10B981' } },
          { value: 1200000, name: 'Business', itemStyle: { color: '#3B82F6' } },
          { value: 500000, name: 'Investment', itemStyle: { color: '#8B5CF6' } },
          { value: 300000, name: 'Other', itemStyle: { color: '#F59E0B' } }
        ]
      }]
    })
  }
})
</script>
