import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/login.vue'

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
      component: () => import('../views/user/user_dashboard.vue'),
    },
    {
      path: '/staff',
      name: 'staff',
      component: () => import('../views/staff/staff_dashboard.vue'),
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/admin/admin_dashboard.vue'),
    },
    {
      path: '/admin/users',
      name: 'admin_users',
      component: () => import('../views/admin/admin_users.vue'),
    },
    {
      path: '/admin/add_trek',
      name: 'admin_add_trek',
      component: () => import('../views/admin/admin_add_trek.vue'),
    },
    {
      path: '/admin/staff',
      name: 'admin_staff',
      component: () => import('../views/admin/admin_staff.vue'),
    }
  ],
})

export default router
