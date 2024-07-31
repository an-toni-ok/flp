<script setup>
import { computed } from 'vue';
import { useToolbarStore } from '@/stores/toolbar';
import { AreaBorder, AreaCorner } from '@/util';
import AreaDisplayBorder from './AreaDisplayBorder.vue';
import AreaDisplayCorner from './AreaDisplayCorner.vue';

const props = defineProps({
    rect: {
        type: Object,
        required: true,
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

const height = computed(() => {
    return props.rect.height * (toolbarStore.zoom / 100);
})
const width = computed(() => {
    return props.rect.width * (toolbarStore.zoom / 100);
})
const left = computed(() => {
    return props.rect.left * (toolbarStore.zoom / 100);
})
const top = computed(() => {
    return props.rect.top * (toolbarStore.zoom / 100);
})

const border_size = computed(() => {
    return 10 * (toolbarStore.zoom / 100)
})

const cssBorderSize = computed(() => {
    return { borderSize: 10 * (toolbarStore.zoom / 100) }
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
            :class="['svg-' + rect.type, 'base-rect']"
            :style="cssBorderSize"
            fill="transparent"
            @mousedown.stop="$emit('move')" />
        <text 
            :x="left + width / 2" 
            :y="top + 0.25 * 16 + border_size + 10"
            text-anchor="middle">{{ rect.width }}</text>
        <text 
            :x="left + 0.25 * 16 + border_size" 
            :y="top + height / 2"
            text-anchor="start">{{ rect.height }}</text>
        <text 
            :x="left + width - 0.25 * 16 - border_size" 
            :y="top + height / 2"
            text-anchor="end">{{ rect.height }}</text>
        <text 
            :x="left + width / 2" 
            :y="top + height - 0.25 * 16 - border_size"
            text-anchor="middle">{{ rect.width }}</text>
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
</template>

<style scoped>
.base-rect {
    cursor: move;
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