<script setup>
import { PlanningState } from '@/util';
import ProcessOverlay from '@/components/Overlays/ProcessOverlay.vue';
import ProgressButtons from '@/components/Buttons/ProgressButtons.vue';

import { usePlanningStore } from '@/stores/planning';

const planningStore = usePlanningStore();
</script>

<template>
    <div class="expand">
        <ProgressButtons
            @prev="planningStore.setState(PlanningState.Areas)"
            @next="planningStore.setState(PlanningState.Machines)" />
    </div>
    <ProcessOverlay />
</template>

<style scoped>
.expand {
	width: 100%;
    height: 100%;
}
</style>