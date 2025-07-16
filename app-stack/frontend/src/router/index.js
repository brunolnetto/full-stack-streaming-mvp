import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../components/MainLayout.vue'
import DashboardPage from '../pages/DashboardPage.vue'
import TestPage from '../pages/TestPage.vue'
import SettingsPage from '../pages/SettingsPage.vue'
import SampleBackendCall from '../components/SampleBackendCall.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      { path: '', redirect: '/dashboard' },
      { path: 'dashboard', component: DashboardPage },
      { path: 'test', component: TestPage },
      { path: 'settings', component: SettingsPage },
    ]
  },
  { path: '/sample', component: SampleBackendCall }
]

export default createRouter({
  history: createWebHistory(),
  routes,
}) 