import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAreasStore = defineStore('areas', () => {
  const areas = ref([])
  function add(restricted = false) {}
  function remove() {}

  return { areas, add, remove }
})
