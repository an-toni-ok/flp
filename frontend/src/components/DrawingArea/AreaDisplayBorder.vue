<script setup>
import { computed } from 'vue';
import { AreaBorder, AreaCorner } from '@/util';

const props = defineProps({
    type: {
        type: String,
        required: true
    },
    position: {
        type: AreaBorder,
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
    strech: {
        position: AreaCorner
    }
})

const width = computed(() => {
    switch (props.position) {
        case AreaBorder.Top:
            return props.r_width - 2 * props.borderWidth;
        case AreaBorder.Left:
            return props.borderWidth;
        case AreaBorder.Right:
            return props.borderWidth;
        case AreaBorder.Bottom:
            return props.r_width - 2 * props.borderWidth;
    }
})

const height = computed(() => {
    switch (props.position) {
        case AreaBorder.Top:
            return props.borderWidth;
        case AreaBorder.Left:
            return props.r_height - 2 * props.borderWidth;
        case AreaBorder.Right:
            return props.r_height - 2 * props.borderWidth;
        case AreaBorder.Bottom:
            return props.borderWidth;
    }
})

const x = computed(() => {
    switch (props.position) {
        case AreaBorder.Top:
            return props.r_left + props.borderWidth;
        case AreaBorder.Left:
            return props.r_left;
        case AreaBorder.Right:
            return props.r_left + props.r_width - props.borderWidth;
        case AreaBorder.Bottom:
            return props.r_left + props.borderWidth;
    }
})

const y = computed(() => {
    switch (props.position) {
        case AreaBorder.Top:
            return props.r_top;
        case AreaBorder.Left:
            return props.r_top + props.borderWidth;
        case AreaBorder.Right:
            return props.r_top + props.borderWidth;
        case AreaBorder.Bottom:
            return props.r_top + props.r_height - props.borderWidth;
    }
})

</script>

<template>

<rect 
    :class="[position.isX() ? 'dir-x' : 'dir-y', 'border-' + type]" 
    :height="height" 
    :width="width"
    :x="x"
    :y="y"
    @mousedown.stop="$emit('strech', position)" />
</template>

<style scoped>
.dir-x {
    cursor: ew-resize;
}

.dir-y {
    cursor: ns-resize;
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