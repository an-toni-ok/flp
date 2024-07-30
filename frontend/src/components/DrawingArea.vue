<script setup>
import { onMounted, ref, toRaw } from 'vue'
import { useToolbarStore } from '@/stores/toolbar';
import { Tool, DrawingShape, DrawingState, AreaCorner, AreaBorder } from '@/util';

import DrawingInput from '@/components/DrawingArea/DrawingInput.vue';
import AreaDisplay from '@/components/DrawingArea/AreaDisplay.vue';

const toolbarStore = useToolbarStore();

const mouse = ref({x: 0, y: 0})
const start_pos = ref({x: undefined, y: undefined})
const strech_x_axis = ref(false)
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

/**
 * Updates the drawing shape based on the mouse position.
 */
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

/**
 * Streches the drawing shape based on the mouse position,
 * the strech direction is determined by strech_x_axis.
 */
const strech_rect = () => {
    if (strech_x_axis.value) {
        drawing_shape_dimensions.value.left = Math.min(
            start_pos.value.x, mouse.value.x
        );
        drawing_shape_dimensions.value.width = Math.abs(
            mouse.value.x - start_pos.value.x
        );
    } else {
        drawing_shape_dimensions.value.height = Math.abs(
            mouse.value.y - start_pos.value.y
        );
        drawing_shape_dimensions.value.top = Math.min(
            start_pos.value.y, mouse.value.y
        );
    }
}

/**
 * Moves the drawing shape based on the mouse position
 * while taking the offset of the mouse into consideration.
 */
const move_rect = () => {
    drawing_shape_dimensions.value.top = mouse.value.y - mouse_offset_in_area.value.y;
    drawing_shape_dimensions.value.left = mouse.value.x - mouse_offset_in_area.value.x;
}

/**
 * Adds the currently drawn shape to its corresponding array.
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

/**
 * Draws a new shape.
 */
const create_shape_handler = () => {
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

/**
 * Event handler for mouse move that calls redraw methods if
 * it is in a Redraw state.
 * 
 * @param {*} event The mouse move event
 */
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
        case DrawingState.Strech.name:
            strech_rect()
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
    if (drawing_state.value == DrawingState.Strech.name) {
        storeCurrentShape();
        drawing_state.value = DrawingState.Drawing.name;
    }
}

/**
 * Removes a shape from its' array and sets the drawing shape
 * to its values.
 * 
 * @param {*} index The index of the shape in its array
 * @param {*} shape The shape itself
 */
const extract_drawing_shape_from_array = (index, shape) => {
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

/**
 * Starts the moving of a shape
 * 
 * @param {*} index The index of the shape clicked on
 * @param {*} shape The shape clicked on
 */
const move_handler = (index, shape) => {
    extract_drawing_shape_from_array(index, shape)

    // Set the offset of the mouse click for the position 
    // calculation later.
    mouse_offset_in_area.value.x = mouse.value.x - shape.left;
    mouse_offset_in_area.value.y = mouse.value.y - shape.top;

    // Set the drawing state
    drawing_state.value = DrawingState.Move.name;
}

/**
 * Starts the resizing of a shape.
 * 
 * @param {*} index The index of the shape clicked on
 * @param {*} shape The shape clicked on
 * @param {AreaCorner} position The mouse position of the click
 */
const resize_handler = (index, shape, position) => {
    extract_drawing_shape_from_array(index, shape)

    // Set the start position to the opposite side of the cursor
    // (position = cursor position)
    switch (position) {
        case AreaCorner.TopLeft:
            start_pos.value.y = shape.top + shape.height;
            start_pos.value.x = shape.left + shape.width;
            break;
        case AreaCorner.TopRight:
            start_pos.value.y = shape.top + shape.height;
            start_pos.value.x = shape.left;
            break;
        case AreaCorner.BottomLeft:
            start_pos.value.y = shape.top;
            start_pos.value.x = shape.left + shape.width;
            break;
        case AreaCorner.BottomRight:
            start_pos.value.y = shape.top;
            start_pos.value.x = shape.left;
            break;
    }

    // Set the drawing state
    drawing_state.value = DrawingState.Resize.name;
}

const stretch_handler = (index, shape, position) => {
    extract_drawing_shape_from_array(index, shape)

    // Set the start position to the opposite side of the cursor
    // (position = cursor position)
    switch (position) {
        case AreaBorder.Top:
        case AreaBorder.Left:
            start_pos.value.y = shape.top + shape.height;
            start_pos.value.x = shape.left + shape.width;
            break;
        case AreaBorder.Right:
        case AreaBorder.Bottom:
            start_pos.value.y = shape.top;
            start_pos.value.x = shape.left;
            break;
    }

    if (position == AreaBorder.Top || position == AreaBorder.Bottom) {
        strech_x_axis.value = false;
    } else {
        strech_x_axis.value = true;
    }

    // Set the drawing state
    drawing_state.value = DrawingState.Strech.name;
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
        @mousedown="create_shape_handler"
        @mousemove="mouse_move_handler"
        @mouseup="mouse_up_handler"
        ref="drawing_container"
        :class="{ 'raised': mouse_down }" >
        <!-- @touchstart="create_shape_handler"
        @touchmove="update"
        @touchend="mouse_up_handler"> -->
        <!-- <div class="plan-drawing"></div> -->
        <svg class="plan-drawing">
            <AreaDisplay 
                v-for="(area, index) in areas"
                :rect="area"
                @resize="(position) => resize_handler(index, area, position)"
                @strech="(position) => stretch_handler(index, area, position)"
                @move="move_handler(index, area)" />
            <AreaDisplay 
                v-model="restricted_areas" 
                v-for="(area, index) in restricted_areas"
                :rect="area"
                @resize="(position) => resize_handler(index, area, position)"
                @strech="(position) => stretch_handler(index, area, position)"
                @move="move_handler(index, area)" />
            <AreaDisplay 
                v-model="machines" 
                v-for="(machine, index) in machines"
                :rect="machine"
                @move="move_handler(index, machine)" />
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