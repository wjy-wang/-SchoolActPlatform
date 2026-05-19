import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { public: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { public: true }
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/home/index.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/activities',
    name: 'ActivityList',
    component: () => import('@/views/activities/List.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/activities/create',
    name: 'ActivityCreate',
    component: () => import('@/views/activities/Form.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/activities/:id',
    name: 'ActivityDetail',
    component: () => import('@/views/activities/Detail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/activities/:id/edit',
    name: 'ActivityEdit',
    component: () => import('@/views/activities/Form.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my-enrollments',
    name: 'MyEnrollments',
    component: () => import('@/views/activities/MyEnrollments.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my-favorites',
    name: 'MyFavorites',
    component: () => import('@/views/activities/MyFavorites.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my-activities',
    name: 'MyActivities',
    component: () => import('@/views/activities/MyActivities.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/profile/index.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/password',
    name: 'Password',
    component: () => import('@/views/profile/Password.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.meta.public && userStore.isLoggedIn) {
    next('/home')
  } else {
    next()
  }
})

export default router
