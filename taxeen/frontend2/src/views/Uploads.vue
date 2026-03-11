<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Upload Statement</h1>
      <p class="text-gray-600 dark:text-gray-400">Upload your bank statement to extract transactions</p>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Upload Form -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-4">Upload Bank Statement</h3>
        
        <form @submit.prevent="handleUpload" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Select Bank</label>
            <select v-model="form.bank_id" required class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
              <option value="">Select Bank</option>
              <option value="1">GTBank - ****1234</option>
              <option value="2">Access Bank - ****5678</option>
            </select>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">From Date</label>
              <input v-model="form.date_from" type="date" required class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">To Date</label>
              <input v-model="form.date_to" type="date" required class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white" />
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Statement File (PDF)</label>
            <div class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center">
              <svg class="w-12 h-12 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
              <p class="text-sm text-gray-600 dark:text-gray-400">Drop your PDF here or click to browse</p>
              <input type="file" accept=".pdf" class="hidden" id="file-upload" @change="handleFileChange" />
              <label for="file-upload" class="mt-4 inline-flex items-center px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg cursor-pointer">
                Choose File
              </label>
              <p v-if="form.file" class="mt-2 text-sm text-gray-600 dark:text-gray-400">{{ form.file.name }}</p>
            </div>
          </div>
          
          <button type="submit" :disabled="uploading" class="w-full py-3 px-4 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50">
            {{ uploading ? 'Processing...' : 'Upload Statement' }}
          </button>
        </form>
      </div>
      
      <!-- Upload History -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-200 dark:border-gray-700">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-4">Upload History</h3>
        
        <div class="space-y-3">
          <div v-for="upload in uploads" :key="upload.id" class="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-gray-900 dark:text-white">{{ upload.filename }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">{{ upload.bank_name }} • {{ upload.date_range }}</p>
              </div>
              <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
                {{ upload.status }}
              </span>
            </div>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">{{ upload.transactions_count }} transactions extracted</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const uploading = ref(false)

const form = reactive({
  bank_id: '',
  date_from: '',
  date_to: '',
  file: null
})

const uploads = ref([
  { id: 1, filename: 'GTBank_Statement_Dec2025.pdf', bank_name: 'GTBank', date_range: 'Dec 2025', status: 'processed', transactions_count: 45 },
  { id: 2, filename: 'AccessBank_Statement_Nov2025.pdf', bank_name: 'Access Bank', date_range: 'Nov 2025', status: 'processed', transactions_count: 32 },
])

function handleFileChange(event) {
  form.file = event.target.files[0]
}

function handleUpload() {
  uploading.value = true
  // Simulate upload
  setTimeout(() => {
    uploads.value.unshift({
      id: Date.now(),
      filename: form.file?.name || 'statement.pdf',
      bank_name: 'GTBank',
      date_range: 'Jan 2026',
      status: 'processing',
      transactions_count: 0
    })
    uploading.value = false
    form.file = null
  }, 2000)
}
</script>
