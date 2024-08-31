<script setup>
import { computed } from 'vue';
import { AreaCorner } from '@/util';

const props = defineProps({
    type: {
        type: String,
        required: true
    },
    position: {
        type: AreaCorner,
        required: true
    },
    r_height: {
        type: Number,
        required: true
    },
    r_width: {
        type: Number,
        required: true
    },
    r_left: {
        type: Number,
        required: true
    },
    r_top: {
        type: Number,
        required: true
    },
    borderWidth: {
        type: Number,
        default: 10,
    }
})

const emits = defineEmits({
    resize: {
        position: AreaCorner
    }
})

const x = computed(() => {
    switch (props.position) {
        case AreaCorner.TopLeft:
            return props.r_left;
        case AreaCorner.TopRight:
            return props.r_left + props.r_width - props.borderWidth;
        case AreaCorner.BottomLeft:
            return props.r_left;
        case AreaCorner.BottomRight:
            return props.r_left + props.r_width - props.borderWidth;
    }
})

const y = computed(() => {
    switch (props.position) {
        case AreaCorner.TopLeft:
            return props.r_top;
        case AreaCorner.TopRight:
            return props.r_top;
        case AreaCorner.BottomLeft:
            return props.r_top + props.r_height - props.borderWidth;
        case AreaCorner.BottomRight:
            return props.r_top + props.r_height - props.borderWidth;
    }
})

</script>

<template>

<rect 
    :class="[position.isDiagnonalTLtoBR() ? 'point-tlbr' : 'point-trbl', 'border-' + type]" 
    :height="borderWidth" 
    :width="borderWidth"
    :x="x"
    :y="y"
    @mousedown.stop="$emit('resize', position)" />
</template>

<style scoped>
.point-tlbr {
    cursor: nwse-resize;
}

.point-trbl {
    cursor: nesw-resize;
}
	
.border-area {
    fill: var(--color-area);
}

.border-restricted-area {
    fill: var(--color-restricted-area);
}

.border-machine {
    fill: var(--color-machine);
}
</style>