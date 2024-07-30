import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { DrawingShape } from '@/util'

export const useAreasStore = defineStore('areas', () => {
  const areas = ref([])
  const restricted_areas = ref([])
  const machines = ref([])

  function addShape(rect) {
    // StructuredClone needs to be used,
    // otherwise the arrays in the cloned object
    // are just a ref a to the original object and
    // setting one updates both.
    switch (rect.type) {
      case DrawingShape.Area.name:
        areas.value.push(structuredClone(rect))
        break
      case DrawingShape.RestrictedArea.name:
        restricted_areas.value.push(structuredClone(rect))
        break
      case DrawingShape.Machine.name:
        machines.value.push(structuredClone(rect))
        break
    }
  }

  function delShape(index, rect) {
    switch (rect.type) {
      case DrawingShape.Area.name:
        areas.value.splice(index, 1)
        break
      case DrawingShape.RestrictedArea.name:
        restricted_areas.value.splice(index, 1)
        break
      case DrawingShape.Machine.name:
        machines.value.splice(index, 1)
        break
    }
  }

  return { areas, restricted_areas, machines, addShape, delShape }
})
