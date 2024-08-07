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

  function json() {
    let areas_json = []
    let r_areas_json = []

    const get_pos = (pos) => {
      let grid_corrected = pos - 10
      let scale_corrected = grid_corrected / square_dimension.value / 10
      // Make sure only one number is after the point
      return parseFloat(scale_corrected.toFixed(1))
    }

    const get_dim = (dim) => {
      let scale_corrected = Math.round(dim / square_dimension.value) / 10
      // Make sure only one number is after the point
      return parseFloat(scale_corrected.toFixed(1))
    }

    for (const area of areas.value) {
      areas_json.push({
        x_position: get_pos(area.left),
        y_position: get_pos(area.top),
        x_dimension: get_dim(area.width),
        y_dimension: get_dim(area.height)
      })
    }

    for (const area of restricted_areas.value) {
      r_areas_json.push({
        x_position: get_pos(area.left),
        y_position: get_pos(area.top),
        x_dimension: get_dim(area.width),
        y_dimension: get_dim(area.height)
      })
    }

    return {
      areas: areas_json,
      restricted_areas: r_areas_json
    }
  }

  function from(areas_json, r_areas_json) {
    const get_pos = (pos) => {
      let scale_corrected = pos * square_dimension.value * 10
      let grid_corrected = scale_corrected + 10
      // Make sure only one number is after the point
      return parseFloat(grid_corrected.toFixed(1))
    }

    const get_dim = (dim) => {
      let scale_corrected = Math.round(dim * square_dimension.value) * 10
      // Make sure only one number is after the point
      return parseFloat(scale_corrected.toFixed(1))
    }

    for (const area of areas_json) {
      areas.value.push({
        left: get_pos(area.x_position),
        top: get_pos(area.y_position),
        width: get_dim(area.x_dimension),
        height: get_dim(area.y_dimension),
        type: DrawingShape.Area.name
      })
    }

    for (const area of r_areas_json) {
      restricted_areas.value.push({
        left: get_pos(area.x_position),
        top: get_pos(area.y_position),
        width: get_dim(area.x_dimension),
        height: get_dim(area.y_dimension),
        type: DrawingShape.RestrictedArea.name
      })
    }
    console.log(areas.value)
  }

  return {
    areas,
    restricted_areas,
    machines,
    square_dimension,
    drawing_dimensions,
    addShape,
    delShape,
    json,
    from
  }
})
