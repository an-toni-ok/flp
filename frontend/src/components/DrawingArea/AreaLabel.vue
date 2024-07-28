<script setup>
import { computed } from 'vue';

const props = defineProps({
    dimensionNr: {
        type: Number,
        required: true,
    },
    otherDimension: {
        type: Number,
        required: true,
    },
    direction: {
        type: String,
        required: true
    }
})

const outsideLabel = computed(() => {
    return (props.dimensionNr < 100) || (props.otherDimension < 60);
})

</script>

<template>
    <p :class="[ 'label', 'label-' + direction, outsideLabel ? 'label-outside-' + direction : '' ]">
        {{ dimensionNr }}px
    </p>
</template>

<style scoped>
.label {
    position: absolute;
    text-align: center;
    font-size: 1rem;
    line-height: 1rem;
    padding: 0.25rem;
}

.label-top {
    width: 100%;
    top: 0;
}

.label-bottom {
    width: 100%;
    bottom: 0;
}

.label-left {
    height: 100%;
    writing-mode: vertical-lr;
    transform: rotate(180deg);
    left: 0;
}

.label-right {
    height: 100%;
    writing-mode: vertical-lr;
    right: 0;
}

.label-outside-top {
    top: -2rem;
}

.label-outside-bottom {
    bottom: -2rem;
}

.label-outside-left {
    left: -2rem;
}

.label-outside-right {
    right: -2rem;
}
</style>