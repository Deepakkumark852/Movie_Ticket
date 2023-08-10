import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/admin',
      name: 'admin',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/admin.vue')
    },
    {
      path:'/user',
      name:'user',
      component: () => import('../views/user.vue')
    },
    {
      path:'/login',
      name:'login',
      component: () => import('../views/login.vue')

    },
    {
      path:'/register',
      name:'register',
      component: () => import('../views/register.vue')
    },
    {
      path:'/profile',
      name:'profile',
      component: () => import('../views/profile.vue')
    },
  ]
})

export default router
