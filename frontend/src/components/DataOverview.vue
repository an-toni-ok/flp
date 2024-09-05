<script setup>
import { ref } from 'vue';
import { MachineTable, ProcessTable, OpenableTable } from '@/components/library/tables';

const props = defineProps({
    bottom_border_only: {
        type: Boolean,
        default: false
    },
    heading: {
        type: Boolean,
        default: true
    }
})

const machine_table_open = ref(false)
const process_table_open = ref(false)

const toggle_machine_table = () => {
    if (!machine_table_open.value) {
        // Allow only one open because of space contraints.
        process_table_open.value = false;
        machine_table_open.value = true
        return
    }
    machine_table_open.value = false
}
const toggle_process_table = () => {
    if (!process_table_open.value) {
        // Allow only one open because of space contraints.
        machine_table_open.value = false;
        process_table_open.value = true
        return
    }
    process_table_open.value = false
}
</script>

<template>
    <div :class="['tables', bottom_border_only ? 'bottom-border-only' : '']">
        <h2 v-if="heading" class="tables-heading">Datenübersicht </h2>

        <OpenableTable name="Prozesse" 
            :opened="process_table_open"
            @click="toggle_process_table">
            <ProcessTable scroll_start="12.5rem" :show_actions="false" />
        </OpenableTable>
        
        <OpenableTable name="Maschinen" 
            :opened="machine_table_open"
            @click="toggle_machine_table">
            <MachineTable scroll_start="12.5rem" :show_actions="false" />
        </OpenableTable>
    </div>
</template>

<style scoped>
.tables {
    padding: 1.5rem;
    height: fit-content;
    border: 1px solid var(--color-border);
}

.bottom-border-only {
    border: none;
    border-bottom: 1px solid var(--color-border);
}

.tables-heading {
    font-size: 1.125rem;
    margin-bottom: 1rem;
}

.tables > :last-child {
    margin-top: 10px;
}
</style>