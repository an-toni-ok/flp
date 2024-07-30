<script setup>
const props = defineProps({
    rect: {
        type: Object,
        required: true,
    }
})

const emits = defineEmits(['selected'])
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
            :class="'svg-' + rect.type"
            fill="none"
            @mousedown.stop="$emit('selected')" />
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
    </g>
</template>

<style scoped>
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