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

  function _update_dimensions() {
    let x_min = 0
    let y_min = 0
    let x_max = 0
    let y_max = 0
    let min_set = false

    for (const rect of areas.value.concat(restricted_areas.value)) {
      if (x_max < rect.left + rect.width) {
        x_max = rect.left + rect.width
      }
      if (x_min > rect.left) {
        x_min = rect.left
      }
      if (y_max < rect.top + rect.height) {
        y_max = rect.top + rect.height
      }
      if (y_min > rect.top) {
        y_min = rect.top
      }
      if (!min_set) {
        x_min = rect.left
        y_min = rect.top
        min_set = true
      }
    }
    drawing_dimensions.value = {
      x_start: x_min,
      x_end: x_max,
      y_start: y_min,
      y_end: y_max
    }
  }

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

    // Keep track of the dimensions in order to fit the drawing
    // with autozoom later.
    _update_dimensions()
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

    // Keep track of the dimensions in order to fit the drawing
    // with autozoom later.
    _update_dimensions()
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
