<script setup>
import { computed, onUnmounted, ref } from 'vue';
import { PlanningState, get_request } from '@/util';
import { usePlanningStore } from '@/stores/planning';

import AreaPlanUnchangable from '@/components/DrawingArea/AreaPlanUnchangable.vue';

const planningStore = usePlanningStore()

// Slide information
const title = "Optimierung wird ausgeführt";

const minutes = ref(0);
const timeLabel = computed(() => {
    let hours = parseInt(minutes.value / 60);
    let hours_text = hours > 0 ? `${hours} h ` : '';
    return hours_text + `${minutes.value % 60} min`
})

const optimizationFinished = async () => {
    const optimize_result = await get_request('optimize');
    const json_result = await optimize_result.json()
    console.log(json_result)
    if (json_result.status == "COMPLETED") {
        planningStore.setState(PlanningState.Result)
    }
}

let interval = setInterval(() => {
    minutes.value += 1;
    optimizationFinished()
}, 60 * 1000)

onUnmounted(() => {
    clearInterval(interval);
})
</script>

<template>
    <div class="expand">
        <div class="title-container">
            <div class="view-data-header">
                <h1>{{ title }}</h1>
                <p>seit {{ timeLabel }}</p>
            </div>
        </div>

        <div class="main-content">
            <AreaPlanUnchangable :auto-resize="true" />
        </div>
    </div>
</template>

<style scoped>
.expand {
	width: 100%;
    height: 100%;
}

.title-container {
    position: relative;
}

.view-data-header {
    z-index: 3;
    position: absolute;
    top: var(--site-margin-tb);
    left: var(--site-margin-lr);
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

.main-content {
    width: 100%;
    height: 100%;
    background-color: var(--color-background-drawing);
    padding: 10rem;
    position: relative;
}
</style>