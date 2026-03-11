<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-50 to-teal-100 dark:from-gray-900 dark:to-gray-800 py-12 px-4">
    <div class="max-w-4xl w-full">
      <!-- Logo -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-primary-600 dark:text-primary-500">Taxeen</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">Choose your plan</p>
      </div>
      
      <!-- Pricing Cards -->
      <div class="grid md:grid-cols-3 gap-6">
        <!-- Basic -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border-2 border-transparent hover:border-primary-500 transition-colors">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">Basic</h3>
          <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">For individuals</p>
          <div class="mt-4">
            <span class="text-4xl font-bold text-gray-900 dark:text-white">₦2,500</span>
            <span class="text-gray-500 dark:text-gray-400">/year</span>
          </div>
          <ul class="mt-6 space-y-3 text-sm">
            <li class="flex items-center text-gray-600 dark:text-gray-400">
              <CheckIcon class="w-5 h-5 text-primary-500 mr-2" />
              3 Bank Accounts
            </li>
            <li class="flex items-center text-gray-600 dark:text-gray-400">
              <CheckIcon class="w-5 h-5 text-primary-500 mr-2" />
              Basic Tax Reports
            </li>
          </ul>
          <button 
            @click="selectPlan('basic')"
            class="w-full mt-6 py-3 px-4 border-2 border-primary-600 text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20 font-medium rounded-lg transition-colors"
          >
            Select Basic
          </button>
        </div>
        
        <!-- Premium -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border-2 border-primary-500 relative transform scale-105">
          <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary-500 text-white px-4 py-1 rounded-full text-sm font-medium">
            Recommended
          </div>
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">Premium</h3>
          <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">For professionals</p>
          <div class="mt-4">
            <span class="text-4xl font-bold text-primary-600">₦5,000</span>
            <span class="text-gray-500 dark:text-gray-400">/year</span>
          </div>
          <ul class="mt-6 space-y-3 text-sm">
            <li class="flex items-center text-gray-600 dark:text-gray-400">
              <CheckIcon class="w-5 h-5 text-primary-500 mr-2" />
              Unlimited Bank Accounts
            </li>
            <li class="flex items-center text-gray-600 dark:text-gray-400">
              <CheckIcon class="w-5 h-5 text-primary-500 mr-2" />
              Full Tax Reports
            </li>
            <li class="flex items-center text-gray-600 dark:text-gray-400">
              <CheckIcon class="w-5 h-5 text-primary-500 mr-2" />
              Priority Support
            </li>
          </ul>
          <button 
            @click="selectPlan('premium')"
            class="w-full mt-6 py-3 px-4 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors"
          >
            Select Premium
          </button>
        </div>
        
        <!-- Enterprise -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border-2 border-transparent hover:border-primary-500 transition-colors">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">Enterprise</h3>
          <p class="text-gray-500 dark:text-gray-400 text-sm mt-1">For businesses</p>
          <div class="mt-4">
            <span class="text-4xl font-bold text-gray-900 dark:text-white">₦15,000</span>
            <span class="text-gray-500 dark:text-gray-400">/year</span>
          </div>
          <ul class="mt-6 space-y-3 text-sm">
            <li class="flex items-center text-gray-600 dark:text-gray-400">
              <CheckIcon class="w-5 h-5 text-primary-500 mr-2" />
              Everything in Premium
            </li>
            <li class="flex items-center text-gray-600 dark:text-gray-400">
              <CheckIcon class="w-5 h-5 text-primary-500 mr-2" />
              API Access
            </li>
          </ul>
          <button 
            @click="selectPlan('enterprise')"
            class="w-full mt-6 py-3 px-4 border-2 border-primary-600 text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20 font-medium rounded-lg transition-colors"
          >
            Select Enterprise
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const CheckIcon = {
  template: `<svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>`
}

function selectPlan(plan) {
  // Mock payment - in production, integrate Paystack
  authStore.user = authStore.user || {}
  authStore.user.subscription_plan = plan
  authStore.user.subscription_status = 'active'
  router.push('/')
}
</script>
