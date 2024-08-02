import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useTechnologiesStore = defineStore('technologies', () => {
  const technologies = ref([])
  function add(technology) {
    if (!technology) {
      return
    }
    if (technologies.value.includes(technology)) {
      return
    }
    technologies.value.push(technology)
  }
  function remove(technology) {
    if (!technologies.value.includes(technology)) {
      return
    }
    let index = technologies.value.indexOf(technology)
    technologies.value.splice(index, 1)
  }

  return { technologies, add, remove }
})
