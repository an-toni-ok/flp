<script setup>
import { ref, watch } from 'vue'
import AreaLabel from '@/components/DrawingArea/AreaLabel.vue';

const props = defineProps(['dimensions', 'mouse_down'])

const shape = ref(undefined)

watch(
    () => props.dimensions,
    (newValue, _) => {
        shape.value.style.left = newValue.left + "px";
        shape.value.style.top = newValue.top + "px";
        shape.value.style.width = newValue.width + "px";
        shape.value.style.height = newValue.height + "px";
    },
    { deep: true }
)
</script>

<template>
    <div 
        v-show="mouse_down"
        class="drawing-shape" 
        ref="shape"
        :class="dimensions.type" >
        <div class="label-container">
            <AreaLabel 
                :dimension-nr="dimensions.width"
                :other-dimension="dimensions.height"
                direction="top" />
            <AreaLabel 
                :dimension-nr="dimensions.width"
                :other-dimension="dimensions.height"
                direction="bottom" />
            <AreaLabel 
                :dimension-nr="dimensions.height"
                :other-dimension="dimensions.width"
                direction="left" />
            <AreaLabel 
                :dimension-nr="dimensions.height"
                :other-dimension="dimensions.width"
                direction="right" />
        </div>
    </div>
</template>

<style scoped>
.drawing-shape {
    position: absolute;
    width: 0px;
    height: 0px;
    top: 0;
    left: 0;
}

.area {
    border: 10px dashed var(--color-area);
}

.restricted-area {
    border: 10px dashed var(--color-restricted-area);
}

.machine {
    background-color: var(--color-machine);
    border: 10px dashed var(--color-background-area);
}

.label-container {
    position: relative;
    height: 100%;
    width: 100%;
}
</style>