import { ref } from 'vue'
import { defineStore } from 'pinia'
import { Tool } from '@/util'

export const useToolbarStore = defineStore('toolbar', () => {
  const activeTool = ref(Tool.Move.name)
  const zoom = ref(100)

  function setTool(tool) {
    activeTool.value = tool.name
  }

  function setZoom(new_zoom) {
    zoom.value = new_zoom
  }

  return { activeTool, zoom, setTool, setZoom }
})
