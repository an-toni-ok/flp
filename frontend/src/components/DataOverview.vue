<script setup>
import { ref } from 'vue';

import MachineTable from '@/components/Tables/MachineTable.vue';
import ProcessTable from '@/components/Tables/ProcessTable.vue';
import IconButtonDataOverview from '@/components/Buttons/IconButtonDataOverview.vue';
import IconArrowDown from './icons/IconArrowDown.vue';

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
    <div class="tables">
        <h2 class="tables-heading">Datenübersicht</h2>
        <div class="table-container">
            <div class="table-container-header">
                <h3 class="table-container-heading">Prozesse</h3>
                <IconButtonDataOverview
                    help_text="Toggle the display of the inputted process data." 
                    @click="toggle_process_table" >
                    <IconArrowDown />
                </IconButtonDataOverview>
            </div>
            <div class="remove-border-overlap">
                <ProcessTable 
                    v-show="process_table_open"
                    :short_table="true"
                    :show_actions="false" />
            </div>
        </div>
        <div class="table-container">
            <div class="table-container-header">
                <h3 class="table-container-heading">Maschinen</h3>
                <IconButtonDataOverview
                    help_text="Toggle the display of the inputted machine data." 
                    @click="toggle_machine_table" >
                    <IconArrowDown />
                </IconButtonDataOverview>
            </div>
            <MachineTable 
                v-show="machine_table_open"
                :short_table="true"
                :show_actions="false" />
        </div>
    </div>
</template>

<style scoped>
.tables {
    padding: 1.5rem;
    border: 1px solid var(--color-border);
    height: fit-content;
}

.tables-heading {
    font-size: 1.125rem;
    margin-bottom: 1rem;
}

.table-container-header {
    display: flex;
    width: 100%;
    justify-content: space-between;
    align-items: center;
    margin-bottom: -1px;
}

.table-container-heading {
    font-size: 1rem;
    border: 1px solid var(--color-border);
    border-right: none;
    width: 100%;
    height: 2.5rem;
    line-height: 2.5rem;
    padding-inline: 1.5rem;
}

.remove-border-overlap {
    margin-bottom: 10px;
}
</style>