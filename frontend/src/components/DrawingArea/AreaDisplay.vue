<script setup>
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
</script>

<template>
    <g>
        <!-- the svg stroke is painted half inside,
        half outside. Therefore the height, width,
        x and y need to be adjusted. -->
        <rect 
            :height="rect.height - 10"
            :width="rect.width - 10"
            :x="rect.left + 5"
            :y="rect.top + 5"
            :class="['svg-' + rect.type, 'base-rect']"
            fill="transparent"
            @mousedown.stop="$emit('move')" />
        <text 
            :x="rect.left + rect.width / 2" 
            :y="rect.top + 0.25 * 16 + 20"
            text-anchor="middle">{{ rect.width }}</text>
        <text 
            :x="rect.left + 0.25 * 16 + 10" 
            :y="rect.top + rect.height / 2"
            text-anchor="start">{{ rect.height }}</text>
        <text 
            :x="rect.left + rect.width - 0.25 * 16 - 10" 
            :y="rect.top + rect.height / 2"
            text-anchor="end">{{ rect.height }}</text>
        <text 
            :x="rect.left + rect.width / 2" 
            :y="rect.top + rect.height - 0.25 * 16 - 10"
            text-anchor="middle">{{ rect.width }}</text>
        <!-- The following four rectangles are the borders of
        the original rectangle and allow for specific cursor
        changes and click handlers. -->
        <AreaDisplayBorder
            v-for="item in area_borders"
            :type="rect.type"
            :position="item"
            :r_height="rect.height"
            :r_width="rect.width"
            :r_left="rect.left"
            :r_top="rect.top"
            @strech="(position) => $emit('strech', position)" />

        <!-- The following four rectangles are the corners of
        the original rectangle and allow for specific cursor
        changes and click handlers. -->
        <AreaDisplayCorner
            v-for="item in area_corners"
            :type="rect.type"
            :position="item"
            :r_height="rect.height"
            :r_width="rect.width"
            :r_left="rect.left"
            :r_top="rect.top"
            @resize="(position) => $emit('resize', position)" />
    </g>
</template>

<style scoped>
.base-rect {
    cursor: move;
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

text {
    pointer-events: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}
</style>