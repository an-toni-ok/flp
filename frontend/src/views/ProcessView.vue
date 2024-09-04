<script setup>
import { PlanningState, post_request } from '@/util';
import { usePlanningStore } from '@/stores/planning';
import { useProcessesStore } from '@/stores/processes';
import LayoutSplitView from './LayoutSplitView.vue';

import { ProcessOverlay } from '@/components/library/overlays';
import { ProcessTable } from '@/components/library/tables';
import { IconButton } from '@/components/library/buttons';
import { IconPlus, IconRemove } from '@/components/icons';
import { AreaPlanUnchangable } from '@/components/library/drawing';

const processesStore = useProcessesStore();
const planningStore = usePlanningStore();

const progress = async () => {
    const process_result = await post_request(
        'process', 
        processesStore.json()
    );
    console.log(process_result)
    planningStore.setState(PlanningState.Machines);
}
</script>

<template>
    <LayoutSplitView
        title="Produktionsprozesseingabe" 
        :number="2"
        @prev="planningStore.setState(PlanningState.Areas)"
        @next="progress" >
        <template v-slot:header-buttons>
            <IconButton 
                text="Prozessschritt erstellen"
                @click="processesStore.create"
                v-show="!processesStore.inputOverlayOpened">
                <IconPlus />
            </IconButton>
            <IconButton 
                text="Eingabedialog schließen"
                @click="processesStore.inputOverlayOpened = false"
                v-show="processesStore.inputOverlayOpened">
                <IconRemove />
            </IconButton>
        </template>
        <template v-slot:table>
            <ProcessTable />
        </template>
        <template v-slot:side-content>
            <AreaPlanUnchangable :auto-resize="true" />
        </template>
        <template v-slot:overlay>
            <ProcessOverlay />
        </template>
    </LayoutSplitView>
</template>

<style scoped>
</style>