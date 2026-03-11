import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './style.css'

import Home from './views/Home.vue'
import Features from './views/Features.vue'
import Pricing from './views/Pricing.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/features', component: Features },
  { path: '/pricing', component: Pricing },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
