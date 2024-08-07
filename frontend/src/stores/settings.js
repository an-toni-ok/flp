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

  function from(objectives, target_cycle_time, operator_cost) {
    cycle_target_time.value = target_cycle_time
    hourly_operator_cost.value = operator_cost
    investion.value = objectives.invest
    piece_cost.value = objectives.cost_per_part
    area_usage.value = objectives.used_area
    worker_amount.value = objectives.number_operators
  }

  function reset() {
    cycle_target_time.value = 0
    hourly_operator_cost.value = 0

    investion.value = false
    piece_cost.value = false
    area_usage.value = false
    worker_amount.value = false
  }

  return {
    cycle_target_time,
    hourly_operator_cost,
    investion,
    piece_cost,
    area_usage,
    worker_amount,
    json,
    from,
    reset
  }
})
