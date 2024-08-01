import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { DrawingShape } from '@/util'
import { useToolbarStore } from './toolbar'

export const useAreasStore = defineStore('areas', () => {
  const areas = ref([])
  const restricted_areas = ref([])
  const machines = ref([])

  const drawing_dimensions = ref({
    x_start: 0,
    x_end: 0,
    y_start: 0,
    y_end: 0
  })

  const square_dimension = computed(() => {
    const toolbarStore = useToolbarStore()
    return parseInt((20 * toolbarStore.zoom) / 100)
  })

  function addShape(rect) {
    // Keep track of the dimensions in order to fit the drawing
    // with autozoom later.
    if (drawing_dimensions.value.x_end < rect.left + rect.width) {
      drawing_dimensions.value.x_end = rect.left + rect.width
    }
    if (drawing_dimensions.value.y_end < rect.top + rect.height) {
      drawing_dimensions.value.y_end = rect.top + rect.height
    }

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

  return {
    areas,
    restricted_areas,
    machines,
    square_dimension,
    drawing_dimensions,
    addShape,
    delShape
  }
})
