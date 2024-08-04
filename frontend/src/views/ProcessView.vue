<script setup>
import { PlanningState, post_request } from '@/util';
import { usePlanningStore } from '@/stores/planning';
import LayoutSplitView from './LayoutSplitView.vue';

import ProcessOverlay from '@/components/Overlays/ProcessOverlay.vue';
import ToolIconButton from '@/components/Toolbar/ToolIconButton.vue';
import IconPlus from '@/components/icons/IconPlus.vue';

import { useProcessesStore } from '@/stores/processes';
import ProcessTable from '@/components/Tables/ProcessTable.vue';
import AreaPlanUnchangable from '@/components/DrawingArea/AreaPlanUnchangable.vue';
import IconRemove from '@/components/icons/IconRemove.vue';

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