<template>
  <div>
    <div class="mb-6">
      <router-link to="/banks" class="text-primary-600 hover:text-primary-700 text-sm font-medium">← Back to Banks</router-link>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mt-2">Add Bank Account</h1>
      <p class="text-gray-600 dark:text-gray-400">Connect a new bank account to your profile</p>
    </div>
    
    <div class="max-w-xl bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700">
      <form @submit.prevent="handleSubmit" class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Bank Name</label>
          <select 
            v-model="form.bank_name"
            required
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500"
          >
            <option value="">Select Bank</option>
            <option v-for="bank in nigerianBanks" :key="bank.code" :value="bank.name">{{ bank.name }}</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Number</label>
          <input 
            v-model="form.account_number"
            type="text"
            required
            maxlength="10"
            pattern="[0-9]{10}"
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500"
            placeholder="0123456789"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Name</label>
          <input 
            v-model="form.account_name"
            type="text"
            required
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500"
            placeholder="JOHN DOE"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Account Type</label>
          <select 
            v-model="form.account_type"
            required
            class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500"
          >
            <option value="savings">Savings</option>
            <option value="current">Current</option>
          </select>
        </div>
        
        <div v-if="error" class="p-3 bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 rounded-lg text-sm">
          {{ error }}
        </div>
        
        <div class="flex gap-4">
          <router-link 
            to="/banks"
            class="flex-1 py-3 px-4 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-medium rounded-lg text-center hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          >
            Cancel
          </router-link>
          <button 
            type="submit"
            :disabled="loading"
            class="flex-1 py-3 px-4 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            {{ loading ? 'Adding...' : 'Add Account' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useBankStore } from '@/stores/banks'

const router = useRouter()
const bankStore = useBankStore()
const loading = ref(false)
const error = ref('')

const form = reactive({
  bank_name: '',
  account_number: '',
  account_name: '',
  account_type: 'savings'
})

const nigerianBanks = [
  { code: '044', name: 'Access Bank' },
  { code: '011', name: 'First Bank of Nigeria' },
  { code: '058', name: 'Guaranty Trust Bank' },
  { code: '033', name: 'United Bank for Africa' },
  { code: '057', name: 'Zenith Bank' },
  { code: '039', name: 'Stanbic IBTC Bank' },
  { code: '070', name: 'Fidelity Bank' },
  { code: '032', name: 'Union Bank' },
  { code: '050', name: 'Ecobank Nigeria' },
  { code: '035', name: 'Wema Bank' },
  { code: '232', name: 'Sterling Bank' },
  { code: '214', name: 'First City Monument Bank' },
  { code: '090', name: 'Kuda Bank' },
  { code: '100', name: 'Moniepoint MFB' },
]

async function handleSubmit() {
  loading.value = true
  error.value = ''
  
  const result = await bankStore.addBank(form)
  
  if (result.success) {
    router.push('/banks')
  } else {
    error.value = result.message
    // Demo mode: just redirect
    router.push('/banks')
  }
  
  loading.value = false
}
</script>
