<template>
  <div>
    <!-- Hero -->
    <section class="gradient-bg hero-pattern pt-24 pb-16">
      <div class="max-w-7xl mx-auto px-4 text-center py-20">
        <h1 class="text-4xl md:text-6xl font-bold text-white mb-6">
          Calculate Your Nigerian<br>Personal Income Tax
        </h1>
        <p class="text-xl text-emerald-100 mb-8 max-w-2xl mx-auto">
          Upload your bank statement, track transactions, and get accurate tax calculations.
        </p>
        <div class="flex gap-4 justify-center">
          <a href="#" class="px-8 py-4 bg-white text-emerald-600 font-bold rounded-lg hover:bg-gray-100">
            Start Free Trial
          </a>
          <router-link to="/features" class="px-8 py-4 border-2 border-white text-white font-bold rounded-lg hover:bg-white/10">
            Learn More
          </router-link>
        </div>
        <p class="mt-6 text-emerald-200 text-sm">Only ₦5,000/year • 7-day free trial</p>
      </div>
    </section>
    
    <!-- Features -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">How Taxeen Works</h2>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8">
          <div class="text-center p-8 rounded-2xl bg-gray-50">
            <div class="w-16 h-16 bg-emerald-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <svg class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">1. Upload Statement</h3>
            <p class="text-gray-600">Upload your bank statement PDF</p>
          </div>
          
          <div class="text-center p-8 rounded-2xl bg-gray-50">
            <div class="w-16 h-16 bg-emerald-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <svg class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">2. Review Transactions</h3>
            <p class="text-gray-600">We extract and classify automatically</p>
          </div>
          
          <div class="text-center p-8 rounded-2xl bg-gray-50">
            <div class="w-16 h-16 bg-emerald-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <svg class="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">3. Get Tax Report</h3>
            <p class="text-gray-600">Accurate calculation with breakdown</p>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Tax Bands -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4">
        <h2 class="text-3xl font-bold text-gray-900 mb-8 text-center">2026 Nigerian Tax Rates</h2>
        
        <div class="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          <div class="space-y-3">
            <div class="flex justify-between p-4 bg-white rounded-lg">
              <span class="text-gray-600">₦0 - ₦800,000</span>
              <span class="font-bold text-emerald-600">0%</span>
            </div>
            <div class="flex justify-between p-4 bg-white rounded-lg">
              <span class="text-gray-600">₦800,001 - ₦3,000,000</span>
              <span class="font-bold text-emerald-600">15%</span>
            </div>
            <div class="flex justify-between p-4 bg-white rounded-lg">
              <span class="text-gray-600">₦3,000,001 - ₦12,000,000</span>
              <span class="font-bold text-emerald-600">18%</span>
            </div>
          </div>
          <div class="space-y-3">
            <div class="flex justify-between p-4 bg-white rounded-lg">
              <span class="text-gray-600">₦12,000,001 - ₦25,000,000</span>
              <span class="font-bold text-emerald-600">21%</span>
            </div>
            <div class="flex justify-between p-4 bg-white rounded-lg">
              <span class="text-gray-600">₦25,000,001 - ₦50,000,000</span>
              <span class="font-bold text-emerald-600">23%</span>
            </div>
            <div class="flex justify-between p-4 bg-white rounded-lg">
              <span class="text-gray-600">Above ₦50,000,000</span>
              <span class="font-bold text-emerald-600">25%</span>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- CTA -->
    <section class="py-20 gradient-bg hero-pattern">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold text-white mb-4">Ready to Calculate Your Tax?</h2>
        <p class="text-emerald-100 mb-8">Join thousands of Nigerians using Taxeen</p>
        <a href="#" class="inline-block px-8 py-4 bg-white text-emerald-600 font-bold rounded-lg hover:bg-gray-100">
          Get Started Now — Free Trial
        </a>
      </div>
    </section>
  </div>
</template>
