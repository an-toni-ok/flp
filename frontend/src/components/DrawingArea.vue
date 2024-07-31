<script setup>
import { onMounted, ref, toRaw } from 'vue'
import { useToolbarStore } from '@/stores/toolbar';
import { useAreasStore } from '@/stores/areas';
import { Tool, DrawingShape, DrawingState, AreaCorner, AreaBorder } from '@/util';

import DrawingInput from '@/components/DrawingArea/DrawingInput.vue';
import AreaDisplay from '@/components/DrawingArea/AreaDisplay.vue';
import AreaBackground from '@/components/DrawingArea/AreaBackground.vue';

const toolbarStore = useToolbarStore();
const areasStore = useAreasStore()

const mouse = ref({x: 0, y: 0})
const shape_start_point = ref({x: undefined, y: undefined})
const strech_x_axis = ref(false)
const moving_mouse_offset = ref({x: 0, y: 0})

const drawing_area_offset = ref({x: 0, y: 0})
const drawing_state = ref(DrawingState.Waiting.name)
const drawing_container = ref(undefined)
const drawing_border_class = ref("")
const drawing_shape_dimensions = ref({
    height: 0,
    width: 0,
    left: 0,
    top: 0,
    type: undefined,
})

/**
 * Updates the drawing shape based on the mouse position.
 */
const update_rect = () => {
    drawing_shape_dimensions.value.left = Math.min(
        shape_start_point.value.x, mouse.value.x
    );
    drawing_shape_dimensions.value.top = Math.min(
        shape_start_point.value.y, mouse.value.y
    );
    drawing_shape_dimensions.value.width = Math.abs(
        mouse.value.x - shape_start_point.value.x
    );
    drawing_shape_dimensions.value.height = Math.abs(
        mouse.value.y - shape_start_point.value.y
    );
}

/**
 * Streches the drawing shape based on the mouse position,
 * the strech direction is determined by strech_x_axis.
 */
const strech_rect = () => {
    if (strech_x_axis.value) {
        drawing_shape_dimensions.value.left = Math.min(
            shape_start_point.value.x, mouse.value.x
        );
        drawing_shape_dimensions.value.width = Math.abs(
            mouse.value.x - shape_start_point.value.x
        );
    } else {
        drawing_shape_dimensions.value.height = Math.abs(
            mouse.value.y - shape_start_point.value.y
        );
        drawing_shape_dimensions.value.top = Math.min(
            shape_start_point.value.y, mouse.value.y
        );
    }
}

/**
 * Moves the drawing shape based on the mouse position
 * while taking the offset of the mouse into consideration.
 */
const move_rect = () => {
    drawing_shape_dimensions.value.top = mouse.value.y - moving_mouse_offset.value.y;
    drawing_shape_dimensions.value.left = mouse.value.x - moving_mouse_offset.value.x;
}

/**
 * Adds the currently drawn shape to its corresponding array.
 * Makes sure the shape is snapped to the grid.
 */
const storeCurrentShape = () => {
    // vue refs are not clonable
    let current_rect = toRaw(drawing_shape_dimensions.value)
    let x, y;
    [ x, y ] = get_grid_point(current_rect.left, current_rect.top)
    current_rect.left = x;
    current_rect.top = y;

    // Make sure that the shape terminates on a grid intersection
    // coordinate on the x axis
    let width_diff = current_rect.width % areasStore.square_dimension;
    current_rect.width -= width_diff;
    if (width_diff > areasStore.square_dimension / 2) {
        current_rect.width += areasStore.square_dimension
    }

    // Make sure that the shape terminates on a grid intersection
    // coordinate on the y axis
    let height_diff = current_rect.height % areasStore.square_dimension;
    current_rect.height -= height_diff;
    if (height_diff > areasStore.square_dimension / 2) {
        current_rect.height += areasStore.square_dimension
    }
    
    // Adjust the shapes so it's correctly displayed after
    // being stored.
    current_rect.height /= (toolbarStore.zoom / 100)
    current_rect.width /= (toolbarStore.zoom / 100)
    current_rect.left /= (toolbarStore.zoom / 100)
    current_rect.top /= (toolbarStore.zoom / 100)


    areasStore.addShape(current_rect);
}

/**
 * Takes a point and returns the closest grid intersection
 * point to it.
 * 
 * @param {*} x The x coordinate of the original point
 * @param {*} y The y coordinate of the original point
 */
const get_grid_point = (x, y) => {
    let grid_x_diff = (x - areasStore.square_dimension / 2) % areasStore.square_dimension;
    let new_x = x - grid_x_diff;
    if (grid_x_diff > areasStore.square_dimension / 2) {
        new_x += areasStore.square_dimension;
    }

    let grid_y_diff = (y - areasStore.square_dimension / 2) % areasStore.square_dimension;
    let new_y = y - grid_y_diff;
    if (grid_y_diff > areasStore.square_dimension / 2) {
        new_y += areasStore.square_dimension
    }

    return [new_x, new_y]
}

/**
 * Creates a new shape.
 */
const create_shape_handler = () => {
    if (!(toolbarStore.activeTool == Tool.Area.name || toolbarStore.activeTool == Tool.RestrictedArea.name)) {
        return
    }
    [ shape_start_point.value.x, shape_start_point.value.y ] = get_grid_point(mouse.value.x, mouse.value.y);

    drawing_state.value = DrawingState.Drawing.name
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
 * Event handler for mouse move events that calls redraw methods if
 * it is in a Redraw state.
 * 
 * @param {*} event The mouse move event
 */
const mouse_move_handler = (event) => {
    mouse.value.x = event.pageX - drawing_area_offset.value.x
    mouse.value.y = event.pageY - drawing_area_offset.value.y
    if (drawing_state.value == DrawingState.Waiting.name) {
        return;
    }

    switch (drawing_state.value) {
        case DrawingState.Drawing.name:
            update_rect()
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

/**
 * Event handler for mouse up events that stores the current shape 
 * if the area is not in a Waiting State.
 */
const mouse_up_handler = () => {
    if (drawing_state.value == DrawingState.Waiting.name) {
        return;
    }

    switch (drawing_state.value) {
        case DrawingState.Drawing.name:
            if (drawing_shape_dimensions.value.height > 10 || drawing_shape_dimensions.value.width > 10) {
                storeCurrentShape();
            }

            drawing_border_class.value = ""
            break;
        case DrawingState.Move.name:
            storeCurrentShape();
            moving_mouse_offset.value.x = 0
            moving_mouse_offset.value.y = 0
            break;
        case DrawingState.Resize.name:
            storeCurrentShape();
            break;
        case DrawingState.Strech.name:
            storeCurrentShape();
            break;
    }

    drawing_state.value = DrawingState.Waiting.name
}

/**
 * Removes a shape from its' array and sets the drawing shape
 * to its values.
 * 
 * @param {*} index The index of the shape in its array
 * @param {*} shape The shape itself
 */
const extract_drawing_shape_from_array = (index, shape) => {
    areasStore.delShape(index, shape)
    drawing_shape_dimensions.value = shape
    drawing_shape_dimensions.value.height *= (toolbarStore.zoom / 100)
    drawing_shape_dimensions.value.width *= (toolbarStore.zoom / 100)
    drawing_shape_dimensions.value.left *= (toolbarStore.zoom / 100)
    drawing_shape_dimensions.value.top *= (toolbarStore.zoom / 100)
    drawing_border_class.value = drawing_shape_dimensions.value.type;
    drawing_state.value = DrawingState.Selected.name
}

/**
 * A wrapper function that deletes the shape, if the current tool
 * is Delete and otherwise executes the wrapped function.
 * 
 * @param {function} func The function to execute if the current tool is not delete
 * @param {*} index The index of the shape in its array
 * @param {*} shape The shape
 * @param {*} position The position of the mouse when the shape was clicked
 */
const delete_or_action_handler = (func, index, shape, position) => {
    if (toolbarStore.activeTool == Tool.Delete.name) {
        areasStore.delShape(index, shape);
        return;
    }
    func(index, shape, position);
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
    moving_mouse_offset.value.x = mouse.value.x - shape.left;
    moving_mouse_offset.value.y = mouse.value.y - shape.top;

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
            shape_start_point.value.y = shape.top + shape.height;
            shape_start_point.value.x = shape.left + shape.width;
            break;
        case AreaCorner.TopRight:
            shape_start_point.value.y = shape.top + shape.height;
            shape_start_point.value.x = shape.left;
            break;
        case AreaCorner.BottomLeft:
            shape_start_point.value.y = shape.top;
            shape_start_point.value.x = shape.left + shape.width;
            break;
        case AreaCorner.BottomRight:
            shape_start_point.value.y = shape.top;
            shape_start_point.value.x = shape.left;
            break;
    }

    // Set the drawing state
    drawing_state.value = DrawingState.Resize.name;
}

/**
 * Starts the stretching of a shape.
 * 
 * @param {*} index The index of the shape clicked on
 * @param {*} shape The shape clicked on
 * @param {AreaCorner} position The mouse position of the click
 */
const stretch_handler = (index, shape, position) => {
    extract_drawing_shape_from_array(index, shape)

    // Set the start position to the opposite side of the cursor
    // (position = cursor position)
    switch (position) {
        case AreaBorder.Top:
        case AreaBorder.Left:
            shape_start_point.value.y = shape.top + shape.height;
            shape_start_point.value.x = shape.left + shape.width;
            break;
        case AreaBorder.Right:
        case AreaBorder.Bottom:
            shape_start_point.value.y = shape.top;
            shape_start_point.value.x = shape.left;
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
    drawing_area_offset.value.x = container_offset.left;
    drawing_area_offset.value.y = container_offset.top;
})
</script>

<template>
    <div 
        class="drawing-container"
        @mousedown="create_shape_handler"
        @mousemove="mouse_move_handler"
        @mouseup="mouse_up_handler"
        ref="drawing_container" 
        :class="{ 'raised': drawing_state != DrawingState.Waiting.name }">
        <!-- @touchstart="create_shape_handler"
        @touchmove="update"
        @touchend="mouse_up_handler"> -->
        <!-- <div class="plan-drawing"></div> -->
        <svg class="plan-drawing">
            <AreaBackground />
            <AreaDisplay 
                v-for="(area, index) in areasStore.areas"
                :rect="area"
                @resize="(position) => delete_or_action_handler(resize_handler, index, area, position)"
                @strech="(position) => delete_or_action_handler(stretch_handler, index, area, position)"
                @move="delete_or_action_handler(move_handler, index, area)" />
            <AreaDisplay 
                v-for="(area, index) in areasStore.restricted_areas"
                :rect="area"
                @resize="(position) => delete_or_action_handler(resize_handler, index, area, position)"
                @strech="(position) => delete_or_action_handler(stretch_handler, index, area, position)"
                @move="delete_or_action_handler(move_handler, index, area)" />
            <AreaDisplay 
                v-for="(machine, index) in areasStore.machines"
                :rect="machine"
                @move="delete_or_action_handler(move_handler, index, machine)" />
        </svg>
        <DrawingInput 
            :dimensions="drawing_shape_dimensions" 
            :mouse_down="drawing_state != DrawingState.Waiting.name" />
    </div>
</template>

<style scoped>
.drawing-container {
    width: 100%;
    height: 100%;
    position: absolute;
    background-color: var(--color-background-drawing);
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
}
</style>