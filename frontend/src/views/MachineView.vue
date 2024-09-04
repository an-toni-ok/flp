<script setup>
import { PlanningState, post_request } from '@/util';
import { usePlanningStore } from '@/stores/planning';
import { useMachinesStore } from '@/stores/machines';

import LayoutSplitView from './LayoutSplitView.vue';
import { MachineTable } from '@/components/library/tables';
import { MachineOverlay } from '@/components/library/overlays';
import { IconButton } from '@/components/library/buttons';
import { AreaPlanUnchangable } from '@/components/library/drawing';
import { IconPlus, IconRemove } from '@/components/icons';

const machinesStore = useMachinesStore();
const planningStore = usePlanningStore();

const progress = async () => {
    const machines_result = await post_request(
        'machines', 
        machinesStore.machines
    );
    console.log(machines_result)
    planningStore.setState(PlanningState.Configuration);
}
</script>

<template>
    <LayoutSplitView
        title="Maschineneingabe" 
        :number="3"
        @prev="planningStore.setState(PlanningState.Processes)"
        @next="progress" >
        <template v-slot:header-buttons>
            <IconButton 
                text="Maschine erstellen" 
                v-show="!machinesStore.input_overlay_opened"
                @click="machinesStore.create">
                <IconPlus />
            </IconButton>
            <IconButton 
                text="Eingabedialog schließen"
                v-show="machinesStore.input_overlay_opened"
                @click="machinesStore.input_overlay_opened = false">
                <IconRemove />
            </IconButton>
        </template>
        <template v-slot:table>
            <MachineTable />
        </template>
        <template v-slot:side-content>
            <AreaPlanUnchangable :auto-resize="true" />
        </template>
        <template v-slot:overlay>
            <MachineOverlay />
        </template>
    </LayoutSplitView>
</template>

<style scoped>
</style>