<template>
  <div>
    <div class="table-filters">
      <template v-for="col in columns">
        <div v-if="isLowCardinality(col)" :key="col.key + '-dropdown'">
          <label :for="col.key + '-filter'">{{ col.label }}</label>
          <select v-model="dropdownFilters[col.key]" :id="col.key + '-filter'">
            <option value="">All</option>
            <option v-for="val in uniqueValues[col.key]" :key="val" :value="val">{{ val }}</option>
          </select>
        </div>
        <div v-else :key="col.key + '-search'">
          <label :for="col.key + '-search'">{{ col.label }}</label>
          <input v-model="searchFilters[col.key]" :id="col.key + '-search'" placeholder="Search..." />
        </div>
      </template>
    </div>
    <table v-if="pagedRows.length">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key" @click="col.sortable ? sortBy(col.key) : null" :class="{sortable: col.sortable, sorted: sortKey === col.key}">
            {{ col.label }}
            <span v-if="col.sortable">
              <span v-if="sortKey === col.key">{{ sortDir === 'asc' ? '▲' : '▼' }}</span>
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in pagedRows" :key="rowKey(row)">
          <td v-for="col in columns" :key="col.key">
            {{ row[col.key] }}
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>No data to display.</div>
    <div v-if="totalPages > 1" class="pagination">
      <button @click="prevPage" :disabled="page === 1">Prev</button>
      <span>Page {{ page }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="page === totalPages">Next</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
const props = defineProps({
  columns: { type: Array, required: true },
  rows: { type: Array, required: true },
  pageSize: { type: Number, default: 10 },
  sortable: { type: Boolean, default: true },
  rowKey: { type: Function, default: row => row.id || row.route || row.key || JSON.stringify(row) }
})
const page = ref(1)
const sortKey = ref(props.columns.find(c => c.sortable)?.key || props.columns[0].key)
const sortDir = ref('asc')

// Filtering state
const dropdownFilters = ref({})
const searchFilters = ref({})

// Unique values for each column
const uniqueValues = computed(() => {
  const result = {}
  for (const col of props.columns) {
    result[col.key] = Array.from(new Set(props.rows.map(r => r[col.key]).filter(v => v != null))).sort()
  }
  return result
})

function isLowCardinality(col) {
  return uniqueValues.value[col.key].length > 0 && uniqueValues.value[col.key].length <= 10
}

const filteredRows = computed(() => {
  return props.rows.filter(row => {
    // Dropdown filters (exact match)
    for (const col of props.columns) {
      if (isLowCardinality(col) && dropdownFilters.value[col.key]) {
        if (row[col.key] != dropdownFilters.value[col.key]) return false
      }
    }
    // Search filters (substring match, case-insensitive)
    for (const col of props.columns) {
      if (!isLowCardinality(col) && searchFilters.value[col.key]) {
        const val = (row[col.key] || '').toString().toLowerCase()
        if (!val.includes(searchFilters.value[col.key].toLowerCase())) return false
      }
    }
    return true
  })
})

function sortBy(key) {
  if (!props.sortable) return
  if (sortKey.value === key) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortDir.value = 'asc'
  }
  page.value = 1
}

const sortedRows = computed(() => {
  if (!props.sortable) return filteredRows.value
  return [...filteredRows.value].sort((a, b) => {
    let cmp = 0
    if (typeof a[sortKey.value] === 'string') {
      cmp = a[sortKey.value].localeCompare(b[sortKey.value])
    } else {
      cmp = (a[sortKey.value] ?? 0) - (b[sortKey.value] ?? 0)
    }
    return sortDir.value === 'asc' ? cmp : -cmp
  })
})

const totalPages = computed(() => Math.ceil(sortedRows.value.length / props.pageSize) || 1)
const pagedRows = computed(() => {
  const start = (page.value - 1) * props.pageSize
  return sortedRows.value.slice(start, start + props.pageSize)
})
function nextPage() { if (page.value < totalPages.value) page.value++ }
function prevPage() { if (page.value > 1) page.value-- }

watch(() => props.rows, () => { page.value = 1 }, { deep: true })

</script>

<style scoped>
.table-filters {
  display: flex;
  gap: 1em;
  margin-bottom: 1em;
  flex-wrap: wrap;
  align-items: center;
}
.table-filters label {
  margin-right: 0.5em;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 0.5em 1em;
  border-bottom: 1px solid #eee;
  text-align: left;
}
th.sortable {
  cursor: pointer;
  user-select: none;
}
th.sorted {
  background: #f0f0f0;
}
.pagination {
  margin: 1em 0;
  display: flex;
  gap: 1em;
  align-items: center;
}
</style> 