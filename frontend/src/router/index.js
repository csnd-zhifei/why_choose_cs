import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'welcome', component: () => import('../views/WelcomeView.vue') },
  { path: '/quiz', name: 'quiz', component: () => import('../views/QuizView.vue') },
  { path: '/home', name: 'home', component: () => import('../views/HomeView.vue') },
  { path: '/post/:id', name: 'post-detail', component: () => import('../views/PostDetailView.vue') },
  { path: '/create', name: 'post-create', component: () => import('../views/PostCreateView.vue') },
  { path: '/edit/:id', name: 'post-edit', component: () => import('../views/PostCreateView.vue') },
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') },
  { path: '/register', name: 'register', component: () => import('../views/RegisterView.vue') },
  { path: '/profile', name: 'profile', component: () => import('../views/ProfileView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
