import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useMachinesStore = defineStore('machines', () => {
  const machines = ref([])
  const machine_types = ref([])
  function add() {}
  function remove() {}

  return { machines, add, remove, machine_types }
})
