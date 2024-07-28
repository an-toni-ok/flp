<script setup>
import { onMounted, ref, toRaw } from 'vue'
import { useToolbarStore } from '@/stores/toolbar';
import { Tool, DrawingShape } from '@/util';

import DrawingInput from '@/components/DrawingArea/DrawingInput.vue';

const toolbarStore = useToolbarStore();

const mouse = ref({x: 0, y: 0})
const start_pos = ref({x: undefined, y: undefined})

const mouse_down = ref(false)
const element_selected = ref(false)

const areas = ref([])
const restricted_areas = ref([])
const machines = ref([])

const drawing_container = ref(undefined)
const drawing_border_class = ref("")
const drawing_shape_dimensions = ref({
    height: 0,
    width: 0,
    left: 0,
    top: 0,
    type: undefined,
})

const offset = ref({x: 0, y: 0})

const update_rect = () => {
    drawing_shape_dimensions.value.left = Math.min(
        start_pos.value.x, mouse.value.x
    );
    drawing_shape_dimensions.value.top = Math.min(
        start_pos.value.y, mouse.value.y
    );
    drawing_shape_dimensions.value.width = Math.abs(
        mouse.value.x - start_pos.value.x
    );
    drawing_shape_dimensions.value.height = Math.abs(
        mouse.value.y - start_pos.value.y
    );
}

const mouse_down_handler = () => {
    if (element_selected.value) {

    } else {
        start_pos.value.x = mouse.value.x
        start_pos.value.y = mouse.value.y
        mouse_down.value = true
        update_rect()
        switch (toolbarStore.activeTool) {
            case Tool.Area.name:
                drawing_border_class.value = 'area'
                drawing_shape_dimensions.value.type = DrawingShape.Area.name
                break
            case Tool.RestrictedArea.name:
                drawing_border_class.value = 'restricted-area'
                drawing_shape_dimensions.value.type = DrawingShape.RestrictedArea.name
                break
        }
    }

}

const mouse_move_handler = (event) => {
    mouse.value.x = event.pageX - offset.value.x
    mouse.value.y = event.pageY - offset.value.y
    if (mouse_down.value) {
        update_rect()
    }
}

const mouse_up_handler = () => {
    if (mouse_down.value) {
        update_rect()
        // vue refs are not clonable
        let current_rect = toRaw(drawing_shape_dimensions.value)
        // Otherwise the arrays in the cloned object
        // are just a ref a to the original object and
        // setting one updates both.
        switch (current_rect.type) {
            case DrawingShape.Area.name:
                areas.value.push(structuredClone(current_rect))
                break;
            case DrawingShape.RestrictedArea.name:
                restricted_areas.value.push(structuredClone(current_rect))
                break;
            case DrawingShape.Machine.name:
                machines.value.push(structuredClone(current_rect))
                break;
        }

        drawing_border_class.value = ""
        mouse_down.value = false
    }
}

onMounted(() => {
    let container_offset = drawing_container.value.getBoundingClientRect()
    offset.value.x = container_offset.left;
    offset.value.y = container_offset.top;
})
</script>

<template>
    <div 
        class="drawing-container"
        @mousedown="mouse_down_handler"
        @mousemove="mouse_move_handler"
        @mouseup="mouse_up_handler"
        ref="drawing_container"
        :class="{ 'raised': mouse_down }" >
        <!-- @touchstart="mouse_down_handler"
        @touchmove="update"
        @touchend="mouse_up_handler"> -->
        <!-- <div class="plan-drawing"></div> -->
        <svg class="plan-drawing">
            <rect v-for="rect in areas"
                :height="rect.height"
                :width="rect.width"
                :x="rect.left"
                :y="rect.top"
                class="svg-area"
                fill="none"
                @mousedown="console.log('hi')"
                ></rect>
            <rect v-for="rect in restricted_areas"
                :height="rect.height"
                :width="rect.width"
                :x="rect.left"
                :y="rect.top"
                class="svg-restricted-area"
                fill="none"
                @click="console.log('hello')"
                ></rect>
            <rect v-for="rect in machines"
                :height="rect.height"
                :width="rect.width"
                :x="rect.left"
                :y="rect.top"
                class="svg-machine"
                fill="none"
                ></rect>
        </svg>
        <DrawingInput 
            :dimensions="drawing_shape_dimensions" 
            :mouse_down="mouse_down" />
    </div>
</template>

<style scoped>
.drawing-container {
    width: 100%;
    height: 100%;
    position: absolute;
}

.raised {
    z-index: 1;
}

.info {
    padding: 10rem;
}

.plan-drawing {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    background-color: var(--color-background-drawing);
}

.svg-area {
    stroke: var(--color-area);
    stroke-width: 10px;
}

.svg-restricted-area {
    stroke: var(--color-restricted-area);
    stroke-width: 10px;
}

.svg-machine {
    fill: var(--color-machine);
}
</style>