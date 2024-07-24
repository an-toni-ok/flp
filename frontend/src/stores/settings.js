import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', () => {
  const cycle_target_time = ref(0)
  const hourly_operator_cost = ref(0)

  const investion = ref(false)
  const piece_cost = ref(false)
  const area_usage = ref(false)
  const worker_amount = ref(false)

  // const cycle_time = ref(undefined)
  // const hourly_operator_cost = ref(undefined)
  // const investion = ref([])
  // const cycle_time = ref([])
  // function add() {}
  // function remove() {}
  return {
    cycle_target_time,
    hourly_operator_cost,
    investion,
    piece_cost,
    area_usage,
    worker_amount
  }
})
