import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useProcessesStore = defineStore('processes', () => {
  var edit_id = undefined
  const input_machine_time = ref(0)
  const input_manual_time = ref(0)
  const input_technology = ref('')
  const processes = ref([])
  function set() {
    if (edit_id) {
      processes.value[edit_id] = {
        machine_time: input_machine_time.value,
        manual_time: input_manual_time.value,
        technology: input_technology.value
      }
      edit_id = undefined
    } else {
      processes.value.push({
        machine_time: input_machine_time.value,
        manual_time: input_manual_time.value,
        technology: input_technology.value
      })
    }
    input_machine_time.value = 0
    input_manual_time.value = 0
    input_technology.value = ''
  }

  function edit(nr) {
    edit_id = nr
    process = processes.value.at(nr)
    input_machine_time.value = process.machine_time
    input_manual_time.value = process.manual_time
    input_technology.value = process.technology
  }

  return { input_machine_time, input_manual_time, input_technology, processes, set }
})
