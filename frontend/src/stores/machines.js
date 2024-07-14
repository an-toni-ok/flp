import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useMachinesStore = defineStore('machines', () => {
  const machines = ref([])
  function add() {}
  function remove() {}

  return { machines, add, remove }
})
