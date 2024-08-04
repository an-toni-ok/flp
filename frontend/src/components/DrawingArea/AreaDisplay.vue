<script setup>
import { computed } from 'vue';
import { useToolbarStore } from '@/stores/toolbar';
import { useAreasStore } from '@/stores/areas';
import { AreaBorder, AreaCorner } from '@/util';
import AreaDisplayBorder from './AreaDisplayBorder.vue';
import AreaDisplayCorner from './AreaDisplayCorner.vue';

const props = defineProps({
    rect: {
        type: Object,
        required: true,
    },
    zoomActivated: {
        type: Boolean,
        default: true,
    },
    displayOnly: {
        type: Boolean,
        default: false
    }
})

// const emits = defineEmits(['move', 'resize', 'strech'])
const emits = defineEmits({
    move: null, 
    resize: {
        position: AreaBorder
    }, 
    strech: {
        position: AreaCorner
    }
})

let area_borders = [
    AreaBorder.Top,
    AreaBorder.Left,
    AreaBorder.Right,
    AreaBorder.Bottom
]
let area_corners = [
    AreaCorner.TopLeft, 
    AreaCorner.TopRight,
    AreaCorner.BottomLeft,
    AreaCorner.BottomRight
]
const toolbarStore= useToolbarStore()
const areasStore = useAreasStore();

const height = computed(() => {
    if (props.zoomActivated) {
        return props.rect.height * (toolbarStore.zoom / 100);
    }
    return props.rect.height;
})
const width = computed(() => {
    if (props.zoomActivated) {
        return props.rect.width * (toolbarStore.zoom / 100);
    }
    return props.rect.width;
})
const left = computed(() => {
    if (props.zoomActivated) {
        return props.rect.left * (toolbarStore.zoom / 100);
    }
    return (props.rect.left);
})
const top = computed(() => {
    if (props.zoomActivated) {
        return props.rect.top * (toolbarStore.zoom / 100);
    }
    return (props.rect.top);
})

const width_label = computed(() => {
    let value = Math.round(width.value / areasStore.square_dimension)
    let last_digit = value % 10
    return `${ (value - last_digit) / 10 },${ last_digit } m`
})

const height_label = computed(() => {
    let value = Math.round(height.value / areasStore.square_dimension)
    let last_digit = value % 10
    return `${ (value - last_digit) / 10 },${ last_digit } m`
})

const border_size = computed(() => {
    // if (props.zoomActivated) {
    //     return 10 * (toolbarStore.zoom / 100);
    // }
    return 10;
})

const cssBorderSize = computed(() => {
    return { strokeWidth: border_size.value }
})
</script>

<template>
    <g>
        <!-- the svg stroke is painted half inside,
        half outside. Therefore the height, width,
        x and y need to be adjusted. -->
        <rect 
            :height="height - border_size"
            :width="width - border_size"
            :x="left + border_size / 2"
            :y="top + border_size / 2"
            :class="['svg-' + rect.type, 'base-rect', { 'no-cursor-change': displayOnly }]"
            :style="cssBorderSize"
            fill="transparent"
            @mousedown.stop="$emit('move')" />
        <g v-if="!displayOnly">
            <text 
                :x="left + width / 2" 
                :y="top + 0.25 * 16 + border_size + 10"
                text-anchor="middle">{{ width_label }}</text>
            <text 
                :x="left + 0.25 * 16 + border_size" 
                :y="top + height / 2"
                text-anchor="start">{{ height_label }}</text>
            <text 
                :x="left + width - 0.25 * 16 - border_size" 
                :y="top + height / 2"
                text-anchor="end">{{ height_label }}</text>
            <text 
                :x="left + width / 2" 
                :y="top + height - 0.25 * 16 - border_size"
                text-anchor="middle">{{ width_label }}</text>
            <!-- The following four rectangles are the borders of
            the original rectangle and allow for specific cursor
            changes and click handlers. -->
            <AreaDisplayBorder
                v-for="item in area_borders"
                :type="rect.type"
                :position="item"
                :r_height="height"
                :r_width="width"
                :r_left="left"
                :r_top="top"
                :border-width="border_size"
                @strech="(position) => $emit('strech', position)" />

            <!-- The following four rectangles are the corners of
            the original rectangle and allow for specific cursor
            changes and click handlers. -->
            <AreaDisplayCorner
                v-for="item in area_corners"
                :type="rect.type"
                :position="item"
                :r_height="height"
                :r_width="width"
                :r_left="left"
                :r_top="top"
                :border-width="border_size"
                @resize="(position) => $emit('resize', position)" />
        </g>
    </g>
</template>

<style scoped>
.base-rect {
    cursor: move;
}

.no-cursor-change {
    cursor: auto;
}

.svg-area {
    stroke: var(--color-area);
}

.svg-restricted-area {
    stroke: var(--color-restricted-area);
}

.svg-machine {
    fill: var(--color-machine);
    stroke: var(--color-machine);
}

text {
    pointer-events: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}
</style>