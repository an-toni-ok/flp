<script setup>
import { computed } from 'vue';
import { useToolbarStore } from '@/stores/toolbar';

const props = defineProps({
    rect: {
        type: Object,
        required: true,
    },
    number: {
        type: Number,
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

const emits = defineEmits(['move'])

const toolbarStore= useToolbarStore()

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

const border_size = computed(() => {
    if (props.zoomActivated) {
        return 10 * (toolbarStore.zoom / 100);
    }
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
            :class="['svg-machine', 'base-rect', { 'no-cursor-change': displayOnly }]"
            :style="cssBorderSize"
            @mousedown.stop="$emit('move')" />
        <text 
            :x="left + width / 2" 
            :y="top + height /2 + 0.25 * 16"
            text-anchor="middle">{{ number }}</text>
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