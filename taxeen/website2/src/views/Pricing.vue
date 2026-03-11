<template>
  <div class="pt-24">
    <section class="py-20 bg-white">
      <div class="max-w-5xl mx-auto px-4">
        <h1 class="text-4xl font-bold text-gray-900 mb-4 text-center">Simple Pricing</h1>
        <p class="text-gray-600 text-center mb-12">Choose the plan that fits your needs</p>
        
        <div class="grid md:grid-cols-3 gap-8">
          <!-- Basic -->
          <div class="p-6 bg-white border-2 border-gray-200 rounded-2xl">
            <h3 class="text-xl font-bold text-gray-900">Basic</h3>
            <p class="text-gray-500 text-sm">For individuals</p>
            <div class="my-6">
              <span class="text-4xl font-bold">₦2,500</span>
              <span class="text-gray-500">/year</span>
            </div>
            <ul class="space-y-3 mb-6 text-sm">
              <li class="flex items-center text-gray-600">✓ 3 Bank Accounts</li>
              <li class="flex items-center text-gray-600">✓ Basic Tax Reports</li>
              <li class="flex items-center text-gray-600">✓ Email Support</li>
            </ul>
            <button class="w-full py-3 border-2 border-emerald-600 text-emerald-600 rounded-lg font-medium">
              Select Basic
            </button>
          </div>
          
          <!-- Premium -->
          <div class="p-6 bg-white border-2 border-emerald-500 rounded-2xl relative">
            <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-emerald-500 text-white px-4 py-1 rounded-full text-sm font-medium">
              Recommended
            </div>
            <h3 class="text-xl font-bold text-gray-900">Premium</h3>
            <p class="text-gray-500 text-sm">For professionals</p>
            <div class="my-6">
              <span class="text-4xl font-bold text-emerald-600">₦5,000</span>
              <span class="text-gray-500">/year</span>
            </div>
            <ul class="space-y-3 mb-6 text-sm">
              <li class="flex items-center text-gray-600">✓ Unlimited Banks</li>
              <li class="flex items-center text-gray-600">✓ Full Tax Reports</li>
              <li class="flex items-center text-gray-600">✓ Priority Support</li>
              <li class="flex items-center text-gray-600">✓ Tax Filing</li>
            </ul>
            <button class="w-full py-3 bg-emerald-600 text-white rounded-lg font-medium">
              Select Premium
            </button>
          </div>
          
          <!-- Enterprise -->
          <div class="p-6 bg-white border-2 border-gray-200 rounded-2xl">
            <h3 class="text-xl font-bold text-gray-900">Enterprise</h3>
            <p class="text-gray-500 text-sm">For businesses</p>
            <div class="my-6">
              <span class="text-4xl font-bold">₦15,000</span>
              <span class="text-gray-500">/year</span>
            </div>
            <ul class="space-y-3 mb-6 text-sm">
              <li class="flex items-center text-gray-600">✓ Everything in Premium</li>
              <li class="flex items-center text-gray-600">✓ API Access</li>
              <li class="flex items-center text-gray-600">✓ Dedicated Manager</li>
            </ul>
            <button class="w-full py-3 border-2 border-emerald-600 text-emerald-600 rounded-lg font-medium">
              Select Enterprise
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
