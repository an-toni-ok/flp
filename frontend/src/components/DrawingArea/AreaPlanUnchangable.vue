<script setup>
import { AreaBorder, AreaCorner } from '@/util';
import { useAreasStore } from '@/stores/areas';

import AreaDisplay from '@/components/DrawingArea/AreaDisplay.vue';
import { computed } from 'vue';

const areasStore = useAreasStore()

const emits = defineEmits({
    move: {
        index: Number,
        area: Object
    }, 
    resize: {
        index: Number,
        area: Object,
        position: AreaBorder
    }, 
    strech: {
        index: Number,
        area: Object,
        position: AreaCorner
    }
})

const viewboxText = computed(() => {
    let width = areasStore.drawing_dimensions.x_end - areasStore.drawing_dimensions.x_start
    let height = areasStore.drawing_dimensions.y_end - areasStore.drawing_dimensions.y_start
    return `${areasStore.drawing_dimensions.x_start} ${areasStore.drawing_dimensions.y_start} ${width} ${height}`
})
</script>

<template>
    <div class="plan-container" ref="plan_container">
        <svg class="plan-drawing" :viewBox="viewboxText">
            <AreaDisplay 
                v-for="(area, index) in areasStore.areas"
                :rect="area"
                :zoomActivated="false"
                @resize="(position) => $emit('resize', index, area, position)"
                @strech="(position) => $emit('strech', index, area, position)"
                @move="$emit('move', index, area)" />
            <AreaDisplay 
                v-for="(area, index) in areasStore.restricted_areas"
                :rect="area"
                :zoomActivated="false"
                @resize="(position) => $emit('resize', index, area, position)"
                @strech="(position) => $emit('strech', index, area, position)"
                @move="$emit('move', index, area)"  />
            <AreaDisplay 
                v-for="(machine, index) in areasStore.machines"
                :rect="machine"
                :zoomActivated="false"
                @move="$emit('move', index, area)"  />
        </svg>
    </div>
</template>

<style scoped>
.plan-container {
    width: 100%;
    height: 100%;
    background-color: var(--color-background-drawing);
    display: flex;
    justify-content: center;
}

.plan-drawing {
    display: block;
    margin: auto 0;
    padding: 1rem;
}
</style>