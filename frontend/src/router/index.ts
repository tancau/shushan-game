import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './routes'
import { usePlayerStore } from '@/stores/player'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0, behavior: 'smooth' }
  },
})

router.beforeEach(async (to, from, next) => {
  const playerStore = usePlayerStore()

  document.title = to.meta.title ? `${to.meta.title} - 蜀山剑侠传` : '蜀山剑侠传'

  if (to.meta.public) {
    next()
    return
  }

  if (!playerStore.isLoggedIn) {
    await playerStore.fetchStatus()
  }

  if (!playerStore.isLoggedIn) {
    next('/auth/login')
    return
  }

  next()
})

router.afterEach(() => {
  // Scroll handled by scrollBehavior
})

export default router
