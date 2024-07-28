<script setup>
import { onMounted, ref } from 'vue'
import { useToolbarStore } from '@/stores/toolbar';
import { Tool } from '@/util';
import AreaLabel from '@/components/DrawingArea/AreaLabel.vue';

const toolbarStore = useToolbarStore();

const mouse = ref({x: 0, y: 0})
const start_pos = ref({x: undefined, y: undefined})

const mouse_down = ref(false)
const first_position_update = ref(false)
const element_selected = ref(false)

const rects = ref([])
const drawing_shape = ref(undefined)
const drawing_container = ref(undefined)
const drawing_border_class = ref("")
const drawing_shape_display_dimensions = ref({
    height: "0px",
    width: "0px"
})

const offset = ref({x: 0, y: 0})

const update_rect = () => {
    let x_pos = Math.min(start_pos.value.x, mouse.value.x) + "px";
    let y_pos = Math.min(start_pos.value.y, mouse.value.y) + "px";

    let width = Math.abs(mouse.value.x - start_pos.value.x) + "px";
    let height = Math.abs(mouse.value.y - start_pos.value.y) + "px";

    if (drawing_shape.value) {
        drawing_shape.value.style.left = x_pos;
        drawing_shape.value.style.top = y_pos;
        drawing_shape.value.style.width = width;
        drawing_shape_display_dimensions.value.width = width;
        drawing_shape.value.style.height = height;
        drawing_shape_display_dimensions.value.height = height;
    }
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
                break
            case Tool.RestrictedArea.name:
                drawing_border_class.value = 'restricted-area'
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
        ref="drawing_container" >
        <!-- @touchstart="mouse_down_handler"
        @touchmove="update"
        @touchend="mouse_up_handler"> -->
        <!-- <div class="plan-drawing"></div> -->
        <div 
            v-show="mouse_down"
            class="drawing-shape" 
            ref="drawing_shape"
            :class="drawing_border_class" >
            <div class="label-container">
                <AreaLabel 
                    :dimension-text="drawing_shape_display_dimensions.width"
                    direction="top" />
                <AreaLabel 
                    :dimension-text="drawing_shape_display_dimensions.width"
                    direction="bottom" />
                <AreaLabel 
                    :dimension-text="drawing_shape_display_dimensions.height"
                    direction="left" />
                <AreaLabel 
                    :dimension-text="drawing_shape_display_dimensions.height"
                    direction="right" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.drawing-container {
    width: 100%;
    height: 100%;
    position: relative;
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
    background-color: lightblue;
}

.drawing-shape {
    position: absolute;
    width: 0px;
    height: 0px;
    top: 0;
    left: 0;
}

.area {
    border: 10px solid var(--color-area);
}

.restricted-area {
    border: 10px solid var(--color-restricted-area);
}

.machine {
    background-color: var(--color-machine);
}

.label-container {
    position: relative;
    height: 100%;
    width: 100%;
}
</style>