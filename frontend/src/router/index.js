import { createRouter, createWebHistory } from 'vue-router'
import PlanungView from '@/views/PlanungView.vue'
import MethodikView from '@/views/MethodikView.vue'
import InformationView from '@/views/InformationView.vue'
import ContactView from '@/views/ContactView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: PlanungView
    },
    {
      path: '/methodik',
      name: 'methodik',
      component: MethodikView
    },
    {
      path: '/info',
      name: 'info',
      component: InformationView
    },
    {
      path: '/contact',
      name: 'contact',
      component: ContactView
    }
  ]
})

export default router
