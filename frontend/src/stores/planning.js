import { computed } from 'vue'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { PlanningState } from '@/util'

export const usePlanningStore = defineStore('planning', () => {
  const planningState = ref(PlanningState.Areas.name)
  const areasCompleted = ref(false)
  const processesCompleted = ref(false)
  const machinesCompleted = ref(false)
  const settingsCompleted = ref(false)

  function setState(state) {
    if (!(state instanceof PlanningState)) {
      throw new Error('State needs to be instance of PlanningState.')
    }
    planningState.value = state.name
  }

  const isActive = computed(() => {
    return (state) => {
      return planningState.value == state.name
    }
  })

  function setAreasCompletion(isComplete) {
    areasCompleted.value = isComplete
  }
  function setProcessesCompletion(isComplete) {
    processesCompleted.value = isComplete
  }
  function setMachinesCompletion(isComplete) {
    machinesCompleted.value = isComplete
  }
  function setSettingsCompletion(isComplete) {
    settingsCompleted.value = isComplete
  }

  return {
    planningState,
    areasCompleted,
    processesCompleted,
    machinesCompleted,
    settingsCompleted,
    isActive,
    setState,
    setAreasCompletion,
    setProcessesCompletion,
    setMachinesCompletion,
    setSettingsCompletion
  }
})
