<script setup>
import { onMounted, ref, toRaw } from 'vue'
import { useToolbarStore } from '@/stores/toolbar';
import { Tool, DrawingShape, DrawingState } from '@/util';

import DrawingInput from '@/components/DrawingArea/DrawingInput.vue';
import AreaDisplay from '@/components/DrawingArea/AreaDisplay.vue';

const toolbarStore = useToolbarStore();

const mouse = ref({x: 0, y: 0})
const start_pos = ref({x: undefined, y: undefined})
const mouse_offset_in_area = ref({x: 0, y: 0})

const mouse_down = ref(false)
const element_selected = ref(false)

const areas = ref([])
const restricted_areas = ref([])
const machines = ref([])

const drawing_state = ref(DrawingState.Drawing.name)
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

const move_rect = () => {
    drawing_shape_dimensions.value.top = mouse.value.y - mouse_offset_in_area.value.y;
    drawing_shape_dimensions.value.left = mouse.value.x - mouse_offset_in_area.value.x;
}

/**
 * Checks if the mouse is currently within the
 * specified area.
 * 
 * @param {*} height Height of the area
 * @param {*} width Width of the area
 * @param {*} left X position of the area
 * @param {*} top Y position of the area
 */
const is_in_area = (height, width, left, top) => {
    let right = left + width;
    let bottom = top + height;

    let is_in_x = (left <= mouse.value.x) && (mouse.value.x <= right);
    let is_in_y = (top <= mouse.value.y) && (mouse.value.y <= bottom);

    return (is_in_x && is_in_y)
}

/**
 * Adds the currently drawn shape to irs corresponding array.
 */
const storeCurrentShape = () => {
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
}

const mouse_down_handler = () => {
    switch (drawing_state.value) {
        case DrawingState.Drawing.name:
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
            break;
        case DrawingState.Selected.name:
            let height = drawing_shape_dimensions.value.height;
            let width = drawing_shape_dimensions.value.width;
            let top = drawing_shape_dimensions.value.top;
            let left = drawing_shape_dimensions.value.left;

            if (!is_in_area(height, width, left, top)) {
                /** Restore the element */
                storeCurrentShape()
                drawing_state.value = DrawingState.Drawing.name;
                drawing_border_class.value = ""
                return
            }

            if (is_in_area(height - 20, width - 20, left + 10, top + 10)) {
                /** Click outside of border areas -> move */
                mouse_offset_in_area.value.x = mouse.value.x - left;
                mouse_offset_in_area.value.y = mouse.value.y - top;
                drawing_state.value = DrawingState.Move.name;
            } else {
                /** Border was clicked -> resize */
                drawing_state.value = DrawingState.Resize.name;
                // Set the position the rectangle expands from 
                // to the point opposite from the mouse in the
                // rectange.
                if (mouse.value.x - left > width / 2) {
                    start_pos.value.x = left;
                } else {
                    start_pos.value.x = left + width;
                }
                if (mouse.value.y - top > height / 2) {
                    start_pos.value.y = top
                } else {
                    start_pos.value.y = top + height
                }
            }
            break;
    }
}

const mouse_move_handler = (event) => {
    mouse.value.x = event.pageX - offset.value.x
    mouse.value.y = event.pageY - offset.value.y
    switch (drawing_state.value) {
        case DrawingState.Drawing.name:
            if (mouse_down.value) {
                update_rect()
            }
            break;
        case DrawingState.Move.name:
            move_rect()
            break;
        case DrawingState.Resize.name:
            update_rect()
            break;
    }
}

const mouse_up_handler = () => {
    if (mouse_down.value) {
        if (drawing_shape_dimensions.value.height > 10 || drawing_shape_dimensions.value.width > 10) {
            storeCurrentShape();
        }

        drawing_border_class.value = ""
        mouse_down.value = false
    }
    if (drawing_state.value == DrawingState.Move.name) {
        storeCurrentShape();
        drawing_state.value = DrawingState.Drawing.name;
        mouse_offset_in_area.value.x = 0
        mouse_offset_in_area.value.y = 0
    }
    if (drawing_state.value == DrawingState.Resize.name) {
        storeCurrentShape();
        drawing_state.value = DrawingState.Drawing.name;
    }
}

const select_handler = (index, shape) => {
    switch (shape.type) {
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
    drawing_shape_dimensions.value = shape
    drawing_border_class.value = drawing_shape_dimensions.value.type;
    drawing_state.value = DrawingState.Selected.name
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
            <AreaDisplay 
                v-for="(area, index) in areas"
                :rect="area"
                @selected="select_handler(index, area)" />
            <AreaDisplay 
                v-model="restricted_areas" 
                v-for="(area, index) in restricted_areas"
                :rect="area"
                @selected="select_handler(index, area)" />
            <AreaDisplay 
                v-model="machines" 
                v-for="(machine, index) in machines"
                :rect="machine"
                @selected="select_handler(index, machine)" />
        </svg>
        <DrawingInput 
            :dimensions="drawing_shape_dimensions" 
            :mouse_down="mouse_down || drawing_state != DrawingState.Drawing.name" />
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
/* 
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
} */
</style>