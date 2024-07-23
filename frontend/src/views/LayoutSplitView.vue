<script setup>
import { PlanningState } from '@/util';
import MachineOverlay from '@/components/Overlays/MachineOverlay.vue';
import ProgressButtons from '@/components/Buttons/ProgressButtons.vue';
import ToolIconButton from '@/components/Toolbar/ToolIconButton.vue';
import IconPlus from '@/components/icons/IconPlus.vue';
import IconRemove from '@/components/icons/IconRemove.vue';

import { usePlanningStore } from '@/stores/planning';
import { useMachinesStore } from '@/stores/machines';
import MachineTable from '@/components/Tables/MachineTable.vue';

const props = defineProps({
    title: {
        type: String,
        required: true
    },
    number: {
        type: Number,
        required: true
    },
    totalNumber: {
        type: Number,
        default: 5
    },
    prevState: {
        type: PlanningState,
        required: true,
    },
    nextState: {
        type: PlanningState,
        required: true
    }
})

const planningStore = usePlanningStore();
</script>

<template>
    <div class="expand">
        <div class="view-content">
            <div class="view-data">
                <div class="view-data-header">
                    <div class="view-data-name">
                        <h1>{{ title }}</h1>
                        <p>{{ number }}/{{ totalNumber }}</p>
                    </div>
                    <slot name="header-buttons"></slot>
                </div>

                <slot name="table"></slot>
            </div>
            <ProgressButtons
                @prev="planningStore.setState(prevState)"
                @next="planningStore.setState(nextState)" />
        </div>
    </div>
    <slot name="overlay"></slot>
</template>

<style scoped>
.expand {
	width: 100%;
    height: 100%;
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
}

.view-data-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: calc(var(--input-height) + var(--tool-area-padding));
}

.view-data-name {
    display: flex;
    align-items: center;
    background-color: var(--color-background);
    border: 1px solid var(--color-border);
    gap: 2rem;
    padding: var(--tool-area-padding) 1.5rem;
}

.view-data-name > h1 {
    line-height: 1;
    font-size: var(--tool-area-height);
    font-weight: 500;
}

.view-data-name > p {
    line-height: 1;
    font-size: 0.8rem;
}
</style>