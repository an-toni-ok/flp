<script setup>
import { ref } from 'vue';
import { PlanningState } from '@/util';
import ProcessOverlay from '@/components/Overlays/ProcessOverlay.vue';
import ProgressButtons from '@/components/Buttons/ProgressButtons.vue';
import ToolIconButton from '@/components/Toolbar/ToolIconButton.vue';
import IconPlus from '@/components/icons/IconPlus.vue';

import { usePlanningStore } from '@/stores/planning';
import { useProcessesStore } from '@/stores/processes';
import ProcessTable from '@/components/Tables/ProcessTable.vue';
import IconRemove from '@/components/icons/IconRemove.vue';

const planningStore = usePlanningStore();
const processesStore = useProcessesStore();

const opened = ref(false)
</script>

<template>
    <div class="expand">
        <div class="view-content">
            <div class="view-data">
                <div class="view-data-header">
                    <div class="view-data-name">
                        <h1>Produktionsprozesseingabe</h1>
                        <p>2/5</p>
                    </div>
                    <ToolIconButton 
                        help_text="Add a process"
                        @click="processesStore.create"
                        v-show="!processesStore.inputOverlayOpened">
                        <IconPlus />
                    </ToolIconButton>
                    <ToolIconButton 
                        help_text="Close the process input"
                        @click="processesStore.inputOverlayOpened = false"
                        v-show="processesStore.inputOverlayOpened">
                        <IconRemove />
                    </ToolIconButton>
                </div>

                <ProcessTable />
            </div>
            <ProgressButtons
                @prev="planningStore.setState(PlanningState.Areas)"
                @next="planningStore.setState(PlanningState.Machines)" />
        </div>
    </div>
    <ProcessOverlay v-model:opened="opened" />
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