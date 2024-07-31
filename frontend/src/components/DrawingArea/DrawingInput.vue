<script setup>
import { ref, watch } from 'vue'
import AreaLabel from '@/components/DrawingArea/AreaLabel.vue';
import { useAreasStore } from '@/stores/areas';

const props = defineProps(['dimensions', 'mouse_down'])

const shape = ref(undefined)

const areasStore = useAreasStore();

const label_texts = ref({
    height: undefined,
    width: undefined,
})

watch(
    () => props.dimensions,
    (newValue, _) => {
        shape.value.style.left = newValue.left + "px";
        shape.value.style.top = newValue.top + "px";
        shape.value.style.width = newValue.width + "px";
        shape.value.style.height = newValue.height + "px";

        label_texts.value.width = Math.round(newValue.width / areasStore.square_dimension)
        label_texts.value.height = Math.round(newValue.height / areasStore.square_dimension)
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
                :dimension-nr="label_texts.width"
                :other-dimension="label_texts.height"
                direction="top" />
            <AreaLabel 
                :dimension-nr="label_texts.width"
                :other-dimension="label_texts.height"
                direction="bottom" />
            <AreaLabel 
                :dimension-nr="label_texts.height"
                :other-dimension="label_texts.width"
                direction="left" />
            <AreaLabel 
                :dimension-nr="label_texts.height"
                :other-dimension="label_texts.width"
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