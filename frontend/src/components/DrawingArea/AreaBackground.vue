<script setup>
import { useAreasStore } from '@/stores/areas';
import { useToolbarStore } from '@/stores/toolbar';
import { computed } from 'vue';

const areasStore = useAreasStore();
const toolbarStore = useToolbarStore();

const square_dimension_halfed = computed(() => {
    return parseInt(areasStore.square_dimension / 2);
})

</script>

<template>
    <defs>
        <pattern 
            id="bg-pattern" 
            patternUnits="userSpaceOnUse" 
            :width="areasStore.square_dimension * 25" 
            :height="areasStore.square_dimension * 25">
            <!-- x-lines -->
            <line 
                class="strong-line"
                x1='0' 
                :x2='areasStore.square_dimension * 25' 
                :y1='square_dimension_halfed' 
                :y2='square_dimension_halfed' 
                stroke-width='2'/>
            <line 
                v-for="index in [0, 1, 2, 3]"
                class="light-line"
                x1='0' 
                :x2='areasStore.square_dimension * 25' 
                :y1='square_dimension_halfed + (areasStore.square_dimension * (index + 1) * 5)' 
                :y2='square_dimension_halfed + (areasStore.square_dimension * (index + 1)) * 5' 
                stroke-width='2'/>
            <line 
                class="strong-line"
                :x1='square_dimension_halfed' 
                :x2='square_dimension_halfed' 
                y1='0' 
                :y2='areasStore.square_dimension * 25' 
                stroke-width='2' />
            <line 
                v-for="index in [0, 1, 2, 3]"
                class="light-line"
                :x1='square_dimension_halfed  + (areasStore.square_dimension * (index + 1)) * 5' 
                :x2='square_dimension_halfed  + (areasStore.square_dimension * (index + 1)) * 5' 
                y1='0' 
                :y2='areasStore.square_dimension * 25' 
                stroke-width='2' />
        </pattern>
        <pattern
            id="bg-pattern-large" 
            patternUnits="userSpaceOnUse" 
            :width="areasStore.square_dimension * 25" 
            :height="areasStore.square_dimension * 25">
            <line 
                class="very-strong-line"
                x1='0' 
                :x2='areasStore.square_dimension * 25' 
                :y1='square_dimension_halfed' 
                :y2='square_dimension_halfed' 
                stroke-width='2'/>
            <line 
                v-for="index in [0, 1, 2, 3]"
                class="strong-line"
                x1='0' 
                :x2='areasStore.square_dimension * 25' 
                :y1='square_dimension_halfed + (areasStore.square_dimension * (index + 1) * 5)' 
                :y2='square_dimension_halfed + (areasStore.square_dimension * (index + 1) * 5)' 
                stroke-width='2'/>
            <line 
                v-for="index in Array.from({length: 25}, (_, index) => index)"
                class="light-line"
                x1='0' 
                :x2='areasStore.square_dimension * 25' 
                :y1='square_dimension_halfed + (areasStore.square_dimension * (index + 1))' 
                :y2='square_dimension_halfed + (areasStore.square_dimension * (index + 1))' 
                stroke-width='2'/>

            <line 
                class="very-strong-line"
                :x1='square_dimension_halfed' 
                :x2='square_dimension_halfed' 
                :y1='0' 
                :y2='areasStore.square_dimension * 25' 
                stroke-width='2'/>
            <line 
                v-for="index in [0, 1, 2, 3]"
                class="strong-line"
                :x1='square_dimension_halfed + (areasStore.square_dimension * (index + 1) * 5)' 
                :x2='square_dimension_halfed + (areasStore.square_dimension * (index + 1) * 5)' 
                :y1='0' 
                :y2='areasStore.square_dimension * 25' 
                stroke-width='2'/>
            <line 
                v-for="index in Array.from({length: 25}, (_, index) => index)"
                class="light-line"
                :x1='square_dimension_halfed + (areasStore.square_dimension * (index + 1))' 
                :x2='square_dimension_halfed + (areasStore.square_dimension * (index + 1))' 
                :y1='0' 
                :y2='areasStore.square_dimension * 25' 
                stroke-width='2'/>
        </pattern>
    </defs>
    <rect v-if="toolbarStore.zoom < 50"
        fill="url(#bg-pattern)" 
        width="100%" 
        height="100%" />
    <rect v-else
        fill="url(#bg-pattern-large)" 
        width="100%" 
        height="100%" />

</template>

<style scoped>
.very-strong-line {
    stroke: #757575
}


.strong-line {
    stroke: #75757570
}

.light-line {
    stroke: #75757540
}
</style>