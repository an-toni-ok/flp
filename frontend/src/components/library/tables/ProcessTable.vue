<script setup>
import { useProcessesStore } from '@/stores/processes';
import { BaseTable, BaseTableHeading, ProcessTableRow, BaseTableRow } from '@/components/library/tables';

const props = defineProps({
    scroll_start: {
        type: String,
        default: "20rem"
    },
    show_actions: {
        type: Boolean,
        default: true
    }
})

const processesStore = useProcessesStore();

</script>

<template>
    <BaseTable 
        :is_empty="processesStore.processes.length == 0"
        :scroll_start="scroll_start">
        <template v-slot:table-head>
            <!-- Never show action icons for the header -->
            <BaseTableRow>
                <th>Technologie</th>
                <th>Extrazeit Maschine</th>
                <th>Extrazeit Manuell</th>
                <th v-if="show_actions">Aktionen</th>
            </BaseTableRow>
        </template>
        <template v-slot:table-rows>
            <ProcessTableRow
                v-for="(process, index) in processesStore.processes"
                :show_actions="show_actions"
                :process="process"
                :index="index">
            </ProcessTableRow>
        </template>
    </BaseTable>
</template>

<style scoped>
</style>