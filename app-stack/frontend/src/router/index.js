import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../components/HitTable.vue'
import SampleBackendCall from '../components/SampleBackendCall.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/sample', name: 'Sample API', component: SampleBackendCall },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router 