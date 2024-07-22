<script setup>
import { PlanningState } from '@/util';
import AreaView from './AreaView.vue';
import ProcessView from './ProcessView.vue';
import MachineView from './MachineView.vue';
import { usePlanningStore } from '@/stores/planning';

const planningStore = usePlanningStore();
</script>

<template>
    <!-- Not working! -->
    <AreaView v-if="planningStore.isActive(PlanningState.Areas)" />
    <ProcessView v-if="planningStore.isActive(PlanningState.Processes)" />
    <MachineView v-if="planningStore.isActive(PlanningState.Machines)" />
</template>

<style scoped>
</style>