<script setup>
import { ref } from 'vue';

import MachineList from '@/components/Result/MachineList.vue';
import ResultsDisplay from '@/components/Result/ResultsDisplay.vue'
import DrawingArea from '@/components/DrawingArea.vue';

// Slide information
const title = "Optimierungsergebnisse";
const number = ref(1);
const total = ref(3);
</script>

<template>
    <div class="expand">
        <div class="view-content">
            <div class="view-data">
                <div class="view-data-header">
                    <h1>{{ title }}</h1>
                </div>
                <!-- Main content -->
                <ResultsDisplay 
                    v-model:number="number"
                    :total="3" />
                <MachineList />
            </div>
        </div>
        <div class="side-content">
            <DrawingArea />
        </div>
    </div>
</template>

<style scoped>
.expand {
	width: 100%;
    height: 100%;
    display: inline-flex;
    overflow: hidden;
}

.view-content {
    width: fit-content;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-block: var(--site-margin-tb);
    padding-inline: var(--site-margin-lr);
    border-right: 1px solid var(--color-border);
    background-color: var(--color-background);
}

.view-data {
    display: flex;
    flex-direction: column;
    gap:  calc(var(--input-height) + var(--tool-area-padding));;
}

.view-data-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    background-color: var(--color-background);
    border: 1px solid var(--color-border);
    gap: 2rem;
    padding: var(--tool-area-padding) 1.5rem;
}

.view-data-header > h1 {
    line-height: 1;
    font-size: var(--tool-area-height);
    font-weight: 500;
}

.view-data-header > p {
    line-height: 1;
    font-size: 0.8rem;
}

.side-content {
    width: 100%;
    height: 100%;
    position: relative;
}
</style>