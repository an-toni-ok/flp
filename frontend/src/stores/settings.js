import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', () => {
  const cycle_target_time = ref(0)
  const hourly_operator_cost = ref(0)

  const investion = ref(false)
  const piece_cost = ref(false)
  const area_usage = ref(false)
  const worker_amount = ref(false)

  function json() {
    return {
      objectives: {
        invest: investion.value,
        cost_per_part: piece_cost.value,
        used_area: area_usage.value,
        number_operators: worker_amount.value
      },
      target_cycle_time: cycle_target_time.value,
      hourly_operator_cost: hourly_operator_cost.value
    }
  }

  return {
    cycle_target_time,
    hourly_operator_cost,
    investion,
    piece_cost,
    area_usage,
    worker_amount,
    json
  }
})
