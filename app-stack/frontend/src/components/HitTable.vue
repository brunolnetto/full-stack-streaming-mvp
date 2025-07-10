<template>
  <div>
    <h2>Route Hit Counts</h2>
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
import { ref, onMounted } from 'vue'

const hits = ref([])

onMounted(async () => {
  try {
    const res = await fetch('/hits')
    if (res.ok) {
      hits.value = await res.json()
    }
  } catch (e) {
    hits.value = []
  }
})
</script> 