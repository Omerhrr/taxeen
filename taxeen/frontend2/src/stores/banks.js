import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useBankStore = defineStore('banks', () => {
  // State
  const banks = ref([])
  const loading = ref(false)
  const error = ref(null)
  
  // Getters
  const totalBalance = computed(() => {
    return banks.value.reduce((sum, bank) => sum + (bank.current_balance || 0), 0)
  })
  
  const bankCount = computed(() => banks.value.length)
  
  // Actions
  async function fetchBanks() {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get('/bank-accounts')
      banks.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch banks'
    } finally {
      loading.value = false
    }
  }
  
  async function addBank(bankData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/bank-accounts', bankData)
      banks.value.push(response.data)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to add bank'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }
  
  async function deleteBank(bankId) {
    try {
      await api.delete(`/bank-accounts/${bankId}`)
      banks.value = banks.value.filter(b => b.id !== bankId)
      return { success: true }
    } catch (err) {
      return { success: false, message: 'Failed to delete bank' }
    }
  }
  
  return {
    banks,
    loading,
    error,
    totalBalance,
    bankCount,
    fetchBanks,
    addBank,
    deleteBank
  }
})
