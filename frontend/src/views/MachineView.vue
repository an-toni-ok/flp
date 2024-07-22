<script setup>
import { PlanningState } from '@/util';
import MachineOverlay from '@/components/Overlays/MachineOverlay.vue';
import ProgressButtons from '@/components/Buttons/ProgressButtons.vue';

import { usePlanningStore } from '@/stores/planning';

const planningStore = usePlanningStore();
</script>

<template>
    <div class="expand">
        <ProgressButtons
            @prev="planningStore.setState(PlanningState.Processes)"
            @next="planningStore.setState(PlanningState.Configuration)" />
    </div>
    <MachineOverlay />
</template>

<style scoped>
.expand {
	width: 100%;
}
</style>