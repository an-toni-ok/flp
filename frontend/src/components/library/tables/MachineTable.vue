<script setup>
import { useMachinesStore } from '@/stores/machines';
import { BaseTable, BaseTableRow, MachineTableRow } from '@/components/library/tables';

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

const machinesStore = useMachinesStore();

</script>

<template>
    <BaseTable 
        :is_empty="machinesStore.machines.length == 0"
        :scroll_start="scroll_start">
        <template v-slot:table-head>
            <!-- Never show action icons for the header -->
            <BaseTableRow>
                <th>Name</th>
                <th>Stundensatz</th>
                <th>Investitionskosten</th>
                <th>Maschinenzeit</th>
                <th>Breite</th>
                <th>Länge</th>
                <th>Technologien</th>
                <th v-if="show_actions">Aktionen</th>
            </BaseTableRow>
        </template>
        <template v-slot:table-rows>
            <MachineTableRow
                v-for="(machine, index) in machinesStore.machines"
                :show_actions="show_actions"
                :machine="machine"
                :index="index">
            </MachineTableRow>
        </template>
    </BaseTable>
</template>

<style scoped>
</style>