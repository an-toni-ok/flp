import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useMachinesStore = defineStore('machines', () => {
  const input_breite = ref(0)
  const input_laenge = ref(0)

  const input_machine_hourly_cost = ref(0)
  const input_investion_cost = ref(0)
  const input_additional_machine_time = ref('')
  const input_machine_type = ref('')

  const input_technology_value = ref('')
  const input_set_technologies = ref([])

  const machines = ref([])
  const machine_types = ref([
    'test1',
    'test2',
    'test3',
    'test4',
    'test5',
    'test6',
    'test7',
    'test8'
  ])
  function add() {}
  function remove() {}

  return {
    machines,
    input_breite,
    input_laenge,
    input_machine_hourly_cost,
    input_investion_cost,
    input_additional_machine_time,
    input_machine_type,
    input_technology_value,
    input_set_technologies,
    add,
    remove,
    machine_types
  }
})
