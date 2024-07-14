import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useProcessesStore = defineStore('processes', () => {
  const processes = ref([])
  function add() {}
  function remove() {}

  return { processes, add, remove }
})
