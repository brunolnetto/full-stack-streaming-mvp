<template>
  <div>
    <h2>Sample Backend Call</h2>
    <button @click="fetchSample">Call Backend</button>
    <div v-if="response">{{ response }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const response = ref('')

async function fetchSample() {
  const res = await fetch('/api/sample')
  const data = await res.json()
  response.value = data.message
}
</script> 