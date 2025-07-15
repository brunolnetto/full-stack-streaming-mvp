<template>
  <div>
    <h2>
      Route Hit Counts
      <span :style="{color: connected ? 'green' : 'red', marginLeft: '1em'}">
        ● {{ connected ? 'Live' : 'Disconnected' }}
      </span>
    </h2>
    <table v-if="hits.length">
      <thead>
        <tr>
          <th>Route</th>
          <th>Count</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="hit in hits" :key="hit.route">
          <td>{{ hit.route }}</td>
          <td>{{ hit.count }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else>Loading...</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const hits = ref([])
const connected = ref(false)
let ws

onMounted(() => {
  ws = new WebSocket('ws://localhost:8000/ws/hits')
  ws.onopen = () => { connected.value = true }
  ws.onclose = () => { connected.value = false }
  ws.onmessage = (event) => {
    try {
      hits.value = JSON.parse(event.data)
    } catch (e) {
      hits.value = [JSON.parse(event.data)]
    }
  }
})
onUnmounted(() => {
  if (ws) ws.close()
})
</script> 