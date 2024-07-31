<script setup>
import { useAreasStore } from '@/stores/areas';
import { computed } from 'vue';

const areasStore = useAreasStore();

const square_dimension_halfed = computed(() => {
    return parseInt(areasStore.square_dimension / 2);
})
</script>

<template>
    <defs>
        <pattern 
            id="bg-pattern" 
            patternUnits="userSpaceOnUse" 
            :width="areasStore.square_dimension * 4" 
            :height="areasStore.square_dimension * 4">
            <!-- x-lines -->
            <line 
                class="strong-line"
                x1='0' 
                :x2='areasStore.square_dimension * 4' 
                :y1='square_dimension_halfed' 
                :y2='square_dimension_halfed' 
                stroke-width='2'/>
            <line 
                v-for="index in [0, 1, 2]"
                class="light-line"
                x1='0' 
                :x2='areasStore.square_dimension * 4' 
                :y1='square_dimension_halfed + (areasStore.square_dimension * (index + 1))' 
                :y2='square_dimension_halfed + (areasStore.square_dimension * (index + 1))' 
                 
                stroke-width='2'/>
            <line 
                class="strong-line"
                :x1='square_dimension_halfed' 
                :x2='square_dimension_halfed' 
                y1='0' 
                :y2='areasStore.square_dimension * 4' 
                stroke-width='2' />
            <line 
                v-for="index in [0, 1, 2]"
                class="light-line"
                :x1='square_dimension_halfed  + (areasStore.square_dimension * (index + 1))' 
                :x2='square_dimension_halfed  + (areasStore.square_dimension * (index + 1))' 
                y1='0' 
                :y2='areasStore.square_dimension * 4' 
                stroke-width='2' />
        </pattern>
    </defs>
    <rect fill="url(#bg-pattern)" width="100%" height="100%" />

</template>

<style scoped>
.strong-line {
    stroke: #75757580
}

.light-line {
    stroke: #75757540
}
</style>