<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from './layout/Sidebar.vue'
import { useHitsData } from '../composables/useHitsData'

// Example SVG icons (replace with your preferred icon set)
const DashboardIcon = {
  template: '<svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M13 5v6h6m-6 0v6m0 0H7m6 0h6"/></svg>'
}
const TestIcon = {
  template: '<svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M8 12l2 2 4-4"/></svg>'
}
const SettingsIcon = {
  template: '<svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3"/><circle cx="12" cy="12" r="10"/></svg>'
}

const sidebarItems = [
  { id: 'dashboard', label: 'Dashboard', route: '/dashboard', icon: DashboardIcon },
  { id: 'test', label: 'Test', route: '/test', icon: TestIcon },
  { id: 'settings', label: 'Settings', route: '/settings', icon: SettingsIcon }
]

const backendUrl = ref('http://backend:8000')
const theme = ref('light')
const pageSize = ref(10)
const hitsData = useHitsData(backendUrl, pageSize)

const route = useRoute()
const router = useRouter()
const activeId = computed(() => {
  // Map current route to sidebar id
  const match = sidebarItems.find(item => route.path.startsWith(item.route))
  return match ? match.id : ''
})
function handleSidebarActivate(id) {
  const item = sidebarItems.find(i => i.id === id)
  if (item) router.push(item.route)
}
const pageProps = {
  hits: hitsData.hits,
  connected: hitsData.connected,
  loading: hitsData.loading,
  error: hitsData.error,
  search: hitsData.search,
  minCount: hitsData.minCount,
  maxCount: hitsData.maxCount,
  sortKey: hitsData.sortKey,
  sortDir: hitsData.sortDir,
  timeRange: hitsData.timeRange,
  manualRefresh: hitsData.manualRefresh,
  tableColumns: [
    { label: 'Route', key: 'route', sortable: true },
    { label: 'Count', key: 'num_hits', sortable: true }
  ],
  sortedHits: hitsData.sortedHits,
  pageSize,
  backendUrl,
  theme
}
</script>

<template>
  <div class="flex min-h-screen bg-gray-50 font-sans">
    <Sidebar :items="sidebarItems" :active-id="activeId" @activate="handleSidebarActivate" />
    <main class="flex-1 p-8 max-w-4xl mx-auto text-gray-900">
      <router-view v-slot="{ Component }">
        <component :is="Component" v-bind="pageProps" />
      </router-view>
    </main>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style> 