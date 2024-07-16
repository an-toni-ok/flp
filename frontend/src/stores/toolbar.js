import { computed } from 'vue'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { Tool } from '@/util'

export const useToolbarStore = defineStore('toolbar', () => {
  const activeTool = ref(Tool.Move.name)
  const zoom = ref(100)
  let zoom_min = 10
  let zoom_max = 500

  function setTool(tool) {
    activeTool.value = tool.name
  }

  const isActive = computed(() => {
    return (tool) => {
      return activeTool.value == tool.name
    }
  })

  function lowerZoom() {
    let new_value = zoom.value - 10
    if (new_value < zoom_min) {
      return
    }
    zoom.value = new_value
  }

  function raiseZoom() {
    let new_value = zoom.value + 10
    if (new_value > zoom_max) {
      return
    }
    zoom.value = new_value
  }

  return { activeTool, zoom, setTool, lowerZoom, raiseZoom, isActive }
})
