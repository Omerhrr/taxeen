<template>
  <div class="min-h-screen bg-white">
    <!-- Navigation -->
    <nav class="fixed w-full z-50 bg-white/90 backdrop-blur-md border-b border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="text-2xl font-bold text-emerald-600">Taxeen</router-link>
          </div>
          
          <div class="hidden md:flex items-center space-x-8">
            <router-link to="/features" class="text-gray-600 hover:text-gray-900">Features</router-link>
            <router-link to="/pricing" class="text-gray-600 hover:text-gray-900">Pricing</router-link>
            <a href="#" class="text-gray-600 hover:text-gray-900">Blog</a>
            <a href="#" class="text-gray-600 hover:text-gray-900">FAQ</a>
          </div>
          
          <div class="flex items-center space-x-4">
            <a href="#" class="text-gray-600 hover:text-gray-900">Login</a>
            <a href="#" class="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors">
              Get Started
            </a>
          </div>
        </div>
      </div>
    </nav>
    
    <router-view />
    
    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-12">
      <div class="max-w-7xl mx-auto px-4 text-center">
        <h3 class="text-2xl font-bold text-emerald-500 mb-4">Taxeen</h3>
        <p class="text-gray-400 mb-4">Nigerian Personal Tax Intelligence Platform</p>
        <p class="text-gray-500 text-sm">&copy; 2026 Taxeen. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
</script>
