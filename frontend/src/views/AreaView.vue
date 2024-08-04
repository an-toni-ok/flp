<script setup>
import { usePlanningStore } from '@/stores/planning';
import { useAreasStore } from '@/stores/areas';
import { PlanningState, post_request } from '@/util';

import Toolbar from '@/components/Toolbar.vue'
import AreaOverlay from '@/components/Overlays/AreaOverlay.vue';
import DrawingArea from '@/components/DrawingArea.vue';

const planningStore = usePlanningStore();
const areasStore = useAreasStore();

const progress = async () => {
    const area_result = await post_request(
        'area', 
        areasStore.json()
    );
    console.log(area_result)
    planningStore.setState(PlanningState.Processes);
}
</script>

<template>
    <div class="main-display">
        <div class="flow-remover-outer">
            <div class="overlay">
                <Toolbar @next="progress" />
                <AreaOverlay :is-create="true" />
            </div>
        </div>
        <DrawingArea />
    </div>
</template>

<style scoped>
.flow-remover-outer {
    position: absolute;
    height: 100%;
    width: 100%;
    top: 0;
    left: 0;
}

.overlay {
    position: relative;
    height: 100%;
    /* margin: var(--site-margin-tb) var(--site-margin-lr); */
    display: flex;
}

.main-display {
    width: 100%;
    height: 100vh;
	overflow: hidden;
    position: relative;
}
</style>