import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/login.vue'

import { useAuth } from '@/stores/auth'
import { useFlash } from '@/stores/flash'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue'),
    // },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/register.vue'),
    },
    {
      path: '/user',
      name: 'user',
      meta: {role : 'user'},
      component: () => import('../views/user/user_dashboard.vue'),
    },
    {
      path: '/user/mybookings',
      name: 'user_mybookings',
      meta: {role : 'user'},
      component: () => import('../views/user/user_mybookings.vue'),
    },
    {
      path: '/staff',
      name: 'staff',
      meta: {role : 'staff'},
      component: () => import('../views/staff/staff_dashboard.vue'),
    },
    {
      path: '/admin',
      name: 'admin',
      meta: {role : 'admin'},
      component: () => import('../views/admin/admin_dashboard.vue'),
    },
    {
      path: '/admin/users',
      name: 'admin_users',
      meta: {role : 'admin'},
      component: () => import('../views/admin/admin_users.vue'),
    },
    {
      path: '/admin/add_trek',
      name: 'admin_add_trek',
      meta: {role : 'admin'},
      component: () => import('../views/admin/admin_add_trek.vue'),
    },
    {
      path: '/admin/staff',
      name: 'admin_staff',
      meta: {role : 'admin'},
      component: () => import('../views/admin/admin_staff.vue'),
    },
    {
      path: '/admin/treks',
      name: 'admin_treks',
      meta: {role : 'admin'},
      component: () => import('../views/admin/admin_treks.vue'),
    },
    {
      path: '/admin/update_trek/:id',
      name: 'admin_update_trek',
      meta: {role : 'admin'},
      component: () => import('../views/admin/admin_update_trek.vue'),
    }
  ],
})

router.beforeEach((to) => {
  const auth = useAuth()
  const flash = useFlash()
  
  if(!to.meta.role) {
    return true
  }

  if(!auth.isLoggedIn) {
    auth.logout()
    flash.showFlash('You must be logged in to access this page', 'danger')
    return '/'
  }

  if(auth.role !== to.meta.role) {
    flash.showFlash('You are not authorized to access this page', 'danger')
    return `/${auth.role}`
  }

  return true
})

export default router
