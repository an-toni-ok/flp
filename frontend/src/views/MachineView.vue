<script setup>
import { PlanningState } from '@/util';
import { useMachinesStore } from '@/stores/machines';

import LayoutSplitView from './LayoutSplitView.vue';
import MachineTable from '@/components/Tables/MachineTable.vue';
import MachineOverlay from '@/components/Overlays/MachineOverlay.vue';
import ToolIconButton from '@/components/Toolbar/ToolIconButton.vue';

import IconPlus from '@/components/icons/IconPlus.vue';
import IconRemove from '@/components/icons/IconRemove.vue';

const machinesStore = useMachinesStore();
</script>

<template>
    <LayoutSplitView
        title="Maschineneingabe" 
        :number="3"
        :prev-state="PlanningState.Processes"
        :next-state="PlanningState.Configuration">
        <template v-slot:header-buttons>
            <ToolIconButton 
                help_text="Add a machine" 
                v-show="!machinesStore.input_overlay_opened"
                @click="machinesStore.create">
                <IconPlus />
            </ToolIconButton>
            <ToolIconButton 
                help_text="Close the machine input"
                v-show="machinesStore.input_overlay_opened"
                @click="machinesStore.input_overlay_opened = false">
                <IconRemove />
            </ToolIconButton>
        </template>
        <template v-slot:table>
            <MachineTable />
        </template>
        <template v-slot:overlay>
            <MachineOverlay />
        </template>
    </LayoutSplitView>
</template>

<style scoped>
</style>