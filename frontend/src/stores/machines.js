import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useMachinesStore = defineStore('machines', () => {
  const edit_id = ref(undefined)
  const input_overlay_opened = ref(false)

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

  function _get_input_machine() {
    return {
      breite: input_breite.value,
      laenge: input_laenge.value,
      machine_hourly_cost: input_machine_hourly_cost.value,
      investion_cost: input_investion_cost.value,
      additional_machine_time: input_additional_machine_time.value,
      machine_type: input_machine_type.value,
      set_technologies: input_set_technologies.value
    }
  }

  function _unset_inputs() {
    input_breite.value = 0
    input_laenge.value = 0
    input_machine_hourly_cost.value = 0
    input_investion_cost.value = 0
    input_additional_machine_time.value = ''
    input_machine_type.value = ''
    input_technology_value.value = ''
    input_set_technologies.value = []
  }

  function set() {
    if (edit_id.value == 0 || edit_id.value) {
      machines.value[edit_id.value] = _get_input_machine()
      edit_id.value = undefined
    } else {
      machines.value.push(_get_input_machine())
    }
    _unset_inputs()
  }

  function edit(nr) {
    edit_id.value = nr
    var machine = machines.value.at(nr)

    input_breite.value = machine.breite
    input_laenge.value = machine.laenge
    input_machine_hourly_cost.value = machine.machine_hourly_cost
    input_investion_cost.value = machine.investion_cost
    input_additional_machine_time.value = machine.additional_machine_time
    input_machine_type.value = machine.machine_type
    input_technology_value.value = ''
    input_set_technologies.value = machine.set_technologies

    input_overlay_opened.value = true
  }

  function create() {
    edit_id.value = undefined
    _unset_inputs()
    input_overlay_opened.value = true
  }

  function clone(nr) {
    var machine = machines.value.at(nr)
    machines.value.splice(nr, 0, machine)
  }

  function del(nr) {
    machines.value.splice(nr, 1)
  }

  return {
    edit_id,
    input_overlay_opened,
    machines,
    input_breite,
    input_laenge,
    input_machine_hourly_cost,
    input_investion_cost,
    input_additional_machine_time,
    input_machine_type,
    input_technology_value,
    input_set_technologies,
    machine_types,
    set,
    edit,
    create,
    clone,
    del
  }
})
