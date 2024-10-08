import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useProcessesStore = defineStore('processes', () => {
  const edit_id = ref(undefined)
  const inputOverlayOpened = ref(false)
  const input_machine_time = ref(0)
  const input_manual_time = ref(0)
  const input_technology = ref('')
  const processes = ref([])
  function set() {
    if (edit_id.value == 0 || edit_id.value) {
      processes.value[edit_id.value] = {
        machine_time: input_machine_time.value,
        manual_time: input_manual_time.value,
        technology: input_technology.value
      }
      edit_id.value = undefined
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

  function move(nr, isDirectionUp) {
    var other_nr = isDirectionUp ? nr - 1 : nr + 1
    if (other_nr < 0) return
    if (other_nr == processes.value.length) return
    var temp = processes.value[other_nr]
    processes.value[other_nr] = processes.value[nr]
    processes.value[nr] = temp
  }

  function edit(nr) {
    edit_id.value = nr
    var process = processes.value.at(nr)
    input_machine_time.value = process.machine_time
    input_manual_time.value = process.manual_time
    input_technology.value = process.technology
    inputOverlayOpened.value = true
  }

  function create() {
    edit_id.value = undefined
    input_machine_time.value = 0
    input_manual_time.value = 0
    input_technology.value = ''
    inputOverlayOpened.value = true
  }

  function clone(nr) {
    var process = processes.value.at(nr)
    processes.value.splice(nr, 0, process)
  }

  function del(nr) {
    processes.value.splice(nr, 1)
  }

  function json() {
    let json_processes = []
    for (const process of processes.value) {
      json_processes.push({
        technology: process.technology,
        work_content: process.manual_time,
        machine_time: process.machine_time
      })
    }
    return json_processes
  }

  function from(json_processes) {
    for (const process of json_processes) {
      processes.value.push({
        technology: process.technology,
        manual_time: process.work_content,
        machine_time: process.machine_time
      })
    }
  }

  function reset() {
    edit_id.value = undefined
    inputOverlayOpened.value = false
    input_machine_time.value = 0
    input_manual_time.value = 0
    input_technology.value = ''
    processes.value = []
  }

  return {
    edit_id,
    input_machine_time,
    inputOverlayOpened,
    input_manual_time,
    input_technology,
    processes,
    set,
    create,
    edit,
    move,
    clone,
    del,
    json,
    from,
    reset
  }
})
