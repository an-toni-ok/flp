<script setup>
import { PlanningState } from '@/util';
import { usePlanningStore } from '@/stores/planning';

import AreaView from './AreaView.vue';
import ProcessView from './ProcessView.vue';
import MachineView from './MachineView.vue';
import ConfigurationView from './ConfigurationView.vue';
import WaitingView from './WaitingView.vue';
import ResultView from './ResultView.vue';

const planningStore = usePlanningStore();
</script>

<template>
    <AreaView v-if="planningStore.isActive(PlanningState.Areas)" />
    <ProcessView v-if="planningStore.isActive(PlanningState.Processes)" />
    <MachineView v-if="planningStore.isActive(PlanningState.Machines)" />
    <ConfigurationView v-if="planningStore.isActive(PlanningState.Configuration)" />
    <WaitingView v-if="planningStore.isActive(PlanningState.Waiting)" />
    <ResultView v-if="planningStore.isActive(PlanningState.Result)" />
</template>

<style scoped>
</style>