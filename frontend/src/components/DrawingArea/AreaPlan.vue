<script setup>
import { AreaBorder, AreaCorner } from '@/util';
import { useAreasStore } from '@/stores/areas';

import AreaDisplay from '@/components/DrawingArea/AreaDisplay.vue';
import MachineDisplay from '@/components/DrawingArea//MachineDisplay.vue';
import AreaBackground from '@/components/DrawingArea/AreaBackground.vue';

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
</script>

<template>
    <svg class="plan-drawing">
        <AreaBackground />
        <AreaDisplay 
            v-for="(area, index) in areasStore.areas"
            :rect="area"
            @resize="(position) => $emit('resize', index, area, position)"
            @strech="(position) => $emit('strech', index, area, position)"
            @move="$emit('move', index, area)" />
        <AreaDisplay 
            v-for="(area, index) in areasStore.restricted_areas"
            :rect="area"
            @resize="(position) => $emit('resize', index, area, position)"
            @strech="(position) => $emit('strech', index, area, position)"
            @move="$emit('move', index, area)"  />
        <MachineDisplay 
            v-for="(machine, index) in areasStore.machines"
            :rect="machine"
            :number="index + 1"
            @move="$emit('move', index, machine)"  />
    </svg>
</template>

<style scoped>
.plan-drawing {
    width: 100%;
    height: 100%;
    background-color: var(--color-background-drawing);
}
</style>