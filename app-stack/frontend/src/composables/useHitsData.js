import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

export function useHitsData(backendUrlRef, pageSizeRef) {
  const hits = ref([])
  const connected = ref(false)
  const loading = ref(true)
  const error = ref('')
  let ws = null

  // Controls
  const search = ref('')
  const minCount = ref()
  const maxCount = ref()
  const sortKey = ref('route')
  const sortDir = ref('asc')
  const timeRange = ref('all')

  function isInTimeRange(hit) {
    if (!hit.event_time || timeRange.value === 'all') return true
    const now = Date.now()
    const t = new Date(hit.event_time).getTime()
    if (timeRange.value === '1h') return now - t <= 3600_000
    if (timeRange.value === '24h') return now - t <= 86400_000
    if (timeRange.value === '7d') return now - t <= 604800_000
    return true
  }

  const filteredHits = computed(() => {
    return hits.value.filter(hit => {
      const matchesSearch = !search.value || hit.route.toLowerCase().includes(search.value.toLowerCase())
      const matchesMin = minCount.value == null || hit.num_hits >= minCount.value
      const matchesMax = maxCount.value == null || hit.num_hits <= maxCount.value
      const matchesTime = isInTimeRange(hit)
      return matchesSearch && matchesMin && matchesMax && matchesTime
    })
  })

  const sortedHits = computed(() => {
    return [...filteredHits.value].sort((a, b) => {
      let cmp = 0
      if (sortKey.value === 'route') {
        cmp = a.route.localeCompare(b.route)
      } else {
        cmp = a.num_hits - b.num_hits
      }
      return sortDir.value === 'asc' ? cmp : -cmp
    })
  })

  function connectWS() {
    loading.value = true
    error.value = ''
    if (ws) ws.close()
    ws = new WebSocket(`${backendUrlRef.value.replace('http', 'ws')}/ws/hits`)
    ws.onopen = () => { connected.value = true; loading.value = false }
    ws.onclose = () => { connected.value = false }
    ws.onerror = () => { error.value = 'WebSocket connection failed'; loading.value = false }
    ws.onmessage = (event) => {
      try {
        hits.value = JSON.parse(event.data)
      } catch (e) {
        hits.value = [JSON.parse(event.data)]
      }
    }
  }
  function manualRefresh() {
    loading.value = true
    error.value = ''
    fetch(`${backendUrlRef.value}/hits`)
      .then(res => res.json())
      .then(data => { hits.value = data; loading.value = false })
      .catch(() => { error.value = 'Failed to fetch data'; loading.value = false })
  }

  onMounted(connectWS)
  onUnmounted(() => { if (ws) ws.close() })
  watch(backendUrlRef, connectWS)

  return {
    hits,
    connected,
    loading,
    error,
    search,
    minCount,
    maxCount,
    sortKey,
    sortDir,
    timeRange,
    filteredHits,
    sortedHits,
    manualRefresh,
    connectWS,
  }
} 