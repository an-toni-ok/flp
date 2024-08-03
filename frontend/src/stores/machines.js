import { ref, toRaw } from 'vue'
import { defineStore } from 'pinia'

export const useMachinesStore = defineStore('machines', () => {
  const edit_id = ref(undefined)
  const input_overlay_opened = ref(false)

  const input_name = ref('')
  const input_breite = ref(0)
  const input_laenge = ref(0)

  const input_machine_hourly_cost = ref(0)
  const input_investion_cost = ref(0)
  const input_additional_machine_time = ref(0)

  const input_technology_value = ref('')
  const input_set_technologies = ref([])

  const machines = ref([])

  function _get_input_machine() {
    return {
      name: input_name.value,
      x_dimension: input_breite.value,
      y_dimension: input_laenge.value,
      x_position: 0,
      y_position: 0,
      rotation: 0,
      hourly_rate: input_machine_hourly_cost.value,
      investion_cost: input_investion_cost.value,
      additional_machine_time: input_additional_machine_time.value,
      technologies: Array.from(input_set_technologies.value)
    }
  }

  function _unset_inputs() {
    input_name.value = ''
    input_breite.value = 0
    input_laenge.value = 0
    input_machine_hourly_cost.value = 0
    input_investion_cost.value = 0
    input_additional_machine_time.value = 0
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

    input_name.value = machine.name
    input_breite.value = machine.x_dimension
    input_laenge.value = machine.y_dimension
    input_machine_hourly_cost.value = machine.hourly_rate
    input_investion_cost.value = machine.investion_cost
    input_additional_machine_time.value = machine.additional_machine_time
    input_technology_value.value = ''
    input_set_technologies.value = Array.from(machine.technologies)

    input_overlay_opened.value = true
  }

  function create() {
    edit_id.value = undefined
    _unset_inputs()
    input_overlay_opened.value = true
  }

  function clone(nr) {
    // vue refs are not clonable
    var temp_machine = toRaw(machines.value.at(nr))
    // Otherwise the arrays in the cloned object
    // are just a ref a to the original object and
    // setting one updates both.
    var machine = structuredClone(temp_machine)
    machines.value.splice(nr, 0, machine)
  }

  function del(nr) {
    machines.value.splice(nr, 1)
  }

  return {
    edit_id,
    input_overlay_opened,
    machines,
    input_name,
    input_breite,
    input_laenge,
    input_machine_hourly_cost,
    input_investion_cost,
    input_additional_machine_time,
    input_technology_value,
    input_set_technologies,
    set,
    edit,
    create,
    clone,
    del
  }
})
