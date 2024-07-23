<script setup>
import { PlanningState } from '@/util';
import LayoutSplitView from './LayoutSplitView.vue';

import ProcessOverlay from '@/components/Overlays/ProcessOverlay.vue';
import ToolIconButton from '@/components/Toolbar/ToolIconButton.vue';
import IconPlus from '@/components/icons/IconPlus.vue';

import { useProcessesStore } from '@/stores/processes';
import ProcessTable from '@/components/Tables/ProcessTable.vue';
import IconRemove from '@/components/icons/IconRemove.vue';

const processesStore = useProcessesStore();
</script>

<template>
    <LayoutSplitView
        title="Produktionsprozesseingabe" 
        :number="2"
        :prev-state="PlanningState.Areas"
        :next-state="PlanningState.Machines">
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
        <template v-slot:overlay>
            <ProcessOverlay />
        </template>
    </LayoutSplitView>
</template>

<style scoped>
</style>