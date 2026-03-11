<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Tax Reports</h1>
      <p class="text-gray-600 dark:text-gray-400">Generate your Nigerian personal income tax reports</p>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Report Form -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-4">Generate Report</h3>
        
        <form @submit.prevent="generateReport" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Tax Year</label>
            <select v-model="form.year" class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
              <option value="2026">2026</option>
              <option value="2025">2025</option>
              <option value="2024">2024</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Annual Rent Paid (₦)</label>
            <input v-model="form.annual_rent" type="number" class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Pension Contribution (₦)</label>
            <input v-model="form.pension" type="number" class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">NHF Contribution (₦)</label>
            <input v-model="form.nhf" type="number" class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" />
          </div>
          
          <button type="submit" class="w-full py-3 px-4 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors">
            Generate Report
          </button>
        </form>
      </div>
      
      <!-- Report Result -->
      <div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700">
        <div v-if="report" class="space-y-6">
          <div>
            <h3 class="font-semibold text-gray-900 dark:text-white mb-4">Tax Summary - {{ report.tax_year }}</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <p class="text-sm text-gray-500 dark:text-gray-400">Gross Income</p>
                <p class="text-xl font-bold text-gray-900 dark:text-white">{{ formatCurrency(report.gross_income) }}</p>
              </div>
              <div class="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <p class="text-sm text-gray-500 dark:text-gray-400">Total Deductions</p>
                <p class="text-xl font-bold text-gray-900 dark:text-white">{{ formatCurrency(report.total_deductions) }}</p>
              </div>
              <div class="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <p class="text-sm text-gray-500 dark:text-gray-400">Chargeable Income</p>
                <p class="text-xl font-bold text-gray-900 dark:text-white">{{ formatCurrency(report.chargeable_income) }}</p>
              </div>
              <div class="p-4 bg-primary-50 dark:bg-primary-900/30 rounded-lg">
                <p class="text-sm text-primary-600 dark:text-primary-400">Tax Payable</p>
                <p class="text-2xl font-bold text-primary-600 dark:text-primary-400">{{ formatCurrency(report.tax_payable) }}</p>
              </div>
            </div>
          </div>
          
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-3">Tax Breakdown by Band</h4>
            <div class="space-y-2">
              <div v-for="band in report.tax_bands" :key="band.band" class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div>
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ band.band }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ band.rate }} rate</p>
                </div>
                <p class="font-medium text-gray-900 dark:text-white">{{ formatCurrency(band.tax) }}</p>
              </div>
            </div>
          </div>
          
          <div class="flex gap-3">
            <button class="flex-1 py-2 px-4 border border-primary-600 text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20 font-medium rounded-lg">
              Export PDF
            </button>
            <button class="flex-1 py-2 px-4 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-medium rounded-lg">
              Export CSV
            </button>
          </div>
        </div>
        
        <div v-else class="text-center py-12">
          <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <p class="text-gray-500 dark:text-gray-400">Select a year and generate your tax report</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const form = reactive({
  year: '2026',
  annual_rent: 1200000,
  pension: 680000,
  nhf: 85000
})

const report = ref(null)

function generateReport() {
  // Mock Nigerian tax calculation
  const grossIncome = 8500000
  const deductions = form.annual_rent * 0.2 + form.pension + form.nhf
  const chargeable = Math.max(0, grossIncome - Math.min(deductions, 500000))
  
  // 2026 Nigerian tax bands
  let tax = 0
  let remaining = chargeable
  const bands = []
  
  const taxBands = [
    { min: 0, max: 800000, rate: 0 },
    { min: 800000, max: 3000000, rate: 0.15 },
    { min: 3000000, max: 12000000, rate: 0.18 },
    { min: 12000000, max: 25000000, rate: 0.21 },
    { min: 25000000, max: 50000000, rate: 0.23 },
    { min: 50000000, max: Infinity, rate: 0.25 }
  ]
  
  for (const band of taxBands) {
    if (remaining <= 0) break
    const width = band.max - band.min
    const taxable = Math.min(remaining, width)
    const bandTax = taxable * band.rate
    if (bandTax > 0) {
      bands.push({
        band: band.max === Infinity ? `Above ₦${(band.min/1000000).toFixed(0)}M` : `₦${(band.min/1000000).toFixed(1)}M - ₦${(band.max/1000000).toFixed(1)}M`,
        rate: `${(band.rate * 100).toFixed(0)}%`,
        tax: bandTax
      })
      tax += bandTax
    }
    remaining -= taxable
  }
  
  report.value = {
    tax_year: form.year,
    gross_income: grossIncome,
    total_deductions: Math.min(deductions, 500000),
    chargeable_income: chargeable,
    tax_payable: tax,
    effective_rate: ((tax / grossIncome) * 100).toFixed(2),
    tax_bands: bands
  }
}

function formatCurrency(value) {
  return new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN', maximumFractionDigits: 0 }).format(value)
}
</script>
