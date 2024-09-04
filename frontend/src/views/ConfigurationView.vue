<script setup>
import { PlanningState, post_request } from '@/util';
import { usePlanningStore } from '@/stores/planning';
import { useSettingsStore } from '@/stores/settings';

import { ProgressButton } from '@/components/library/buttons';
import { ConfigurationForm } from '@/components/library/forms';
import { DataOverview } from '@/components';
import { AreaPlanUnchangable } from '@/components/library/drawing';

// Slide information
const title = "Optimierungkonfiguration";
const number = 4;
const totalNumber = 4;

const planningStore = usePlanningStore();
const settingsStore = useSettingsStore();

const complete = async () => {
    const objective_result = await post_request(
        'objectives', 
        settingsStore.json()
    );
    console.log(objective_result)
    const optimize_result = await post_request(
        'optimize', 
        undefined
    );
    console.log(optimize_result)
    planningStore.setState(PlanningState.Waiting)
}
</script>

<template>
    <div class="expand">
        <div class="view-content">
            <div class="view-data">
                <div class="view-data-header">
                    <h1>{{ title }}</h1>
                    <p>{{ number }} von {{ totalNumber }}</p>
                </div>
                <!-- Main content -->
                <ConfigurationForm />
                <DataOverview />
            </div>
            <ProgressButton
                @prev="planningStore.setState(PlanningState.Machines)"
                @next="complete"
                :complete="true" />
        </div>
        <div class="side-content">
            <AreaPlanUnchangable :auto-resize="true" />
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
}
</style>