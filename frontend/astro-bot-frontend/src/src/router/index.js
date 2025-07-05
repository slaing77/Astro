import { createRouter, createWebHistory } from 'vue-router'
import App from '../App.vue'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  { path: '/', component: App },
  { 
    path: '/dashboard', 
    component: Dashboard,
    meta: { requiresAuth: true },  // ✅ mark this route as protected
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    // ✅ Redirect unauthenticated users back to login/register page
    next('/')
  } else {
    next()
  }
})

export default router
