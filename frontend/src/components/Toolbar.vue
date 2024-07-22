<script setup>
import { usePlanningStore } from '@/stores/planning';
import { PlanningState } from '@/util';

import ZoomDisplay from './Toolbar/ZoomDisplay.vue';
import IconsDisplay from './Toolbar/IconsDisplay.vue';
import ProgressButtons from '@/components/Buttons/ProgressButtons.vue';

const planningStore = usePlanningStore();
</script>

<template>
    <div class="actions-container">
        <div class="tool-area">
            <div class="tool-area-name">
                <h1>Flächeneingabe</h1>
                <p>1/5</p>
            </div>
            <IconsDisplay />
            <ZoomDisplay />
        </div>
        <ProgressButtons 
            @next="planningStore.setState(PlanningState.Processes)"
            @prev="" />
    </div>
</template>

<style scoped>
.actions-container {
    position: relative;
    padding-block: var(--site-margin-tb);
    padding-inline: var(--site-margin-lr);
    flex: 1;
    height: 100%;
    display: flex;
    flex-direction: column-reverse;
    justify-content: space-between;
}

.tool-area {
    z-index: 3;
    position: absolute;
    top: var(--site-margin-tb);
    left: var(--site-margin-lr);
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 2rem;
}

.tool-area-name {
    display: flex;
    align-items: center;
    background-color: var(--color-background);
    border: 1px solid var(--color-border);
    gap: 2rem;
    padding: var(--tool-area-padding) 1.5rem;
}

.tool-area-name > h1 {
    line-height: 1;
    font-size: var(--tool-area-height);
    font-weight: 500;
}

.tool-area-name > p {
    line-height: 1;
    font-size: 0.8rem;
}
</style>
