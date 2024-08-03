<script setup>
import { useMachinesStore } from '@/stores/machines';
import MachineTableRow from './MachineTableRow.vue';
import IconButtonTable from '@/components/Buttons/IconButtonTable.vue'
import IconEdit from '@/components/icons/IconEdit.vue';
import IconDuplicate from '@/components/icons/IconDuplicate.vue';
import IconDelete from '@/components/icons/IconDelete.vue';

const props = defineProps({
    short_table: {
        type: Boolean,
        default: false
    },
    show_actions: {
        type: Boolean,
        default: true
    }
})

const machinesStore = useMachinesStore();
</script>

<template>
    <div class="table-container" :class="{ 'short': short_table }">
        <table>
            <tr>
                <th>Name</th>
                <th>Maschinentyp</th>
                <th>Stundensatz</th>
                <th>Investitionskosten</th>
                <th>Maschinenzeit</th>
                <th>Breite</th>
                <th>Länge</th>
                <th>Technologien</th>
                <th colspan="5" v-if="show_actions">Aktionen</th>
            </tr>
            <MachineTableRow 
                v-for="(item, index) in machinesStore.machines"
                :machine="item"
                :show_actions="show_actions" >
                    <IconButtonTable 
                        help_text="Edit this table row"
                        @click="machinesStore.edit(index)">
                        <IconEdit />
                    </IconButtonTable>
                    <IconButtonTable
                        help_text="Duplicate this table row"
                        :focus="false"
                        @click="machinesStore.clone(index)">
                        <IconDuplicate />
                    </IconButtonTable>
                    <IconButtonTable
                        help_text="Delete this table row"
                        :focus="false"
                        @click="machinesStore.del(index)">
                        <IconDelete />
                    </IconButtonTable>
            </MachineTableRow>
        </table>
        <p 
            v-if="!machinesStore.machines.length"
            class="no-data">Zur Zeit sind noch keine Daten in der Tabelle.</p>
    </div>
</template>

<style scoped>
.table-container {
    --scrollbar-width: 6px;
    max-height: calc(100vh - 15rem);
    overflow-y: auto;
    border: 1px solid var(--color-border);
    border-left: none;
    border-right: none;
}

.short {
    max-height: 15rem;
}

.table-container::-webkit-scrollbar {
    width: var(--scrollbar-width);
    border-right: 1px solid var(--color-border);
}

.table-container::-webkit-scrollbar-thumb {
    width: var(--scrollbar-width);
    border-radius: 50px;
    background-color: var(--color-border);
}

table {
    border-collapse: collapse;
    border-spacing: 0;
    padding-left: 1.5rem;
    min-width: 37rem;
    width: 100%;
}

table > tr {
    border: 1px solid var(--color-border);
    height: var(--input-height);
}

table > tr:first-child {
    /* border already set by table container */
    border-top: none;
}

table > tr:last-child {
    /* border already set by table container */
    border-bottom: none;
}

table > tr:only-child {
    /* Set the border if only the table head is set */
    border-bottom: 1px solid var(--color-border);
}

table > tr > th {
    text-align: left;
}

table > tr > th:last-child {
    text-align: center;
}

table > tr > th {
    padding-block: calc(0.75 * var(--default-padding));
}

table > tr > * {
    padding: calc(0.75 * var(--default-padding)) var(--default-padding);
}

table > tr > *:first-child {
    padding-left: 1.5rem;
}

.no-data {
    border: 1px solid var(--color-border);
    border-top: none;
    border-bottom: none;
    padding-inline: 1.5rem;
    padding-block: calc(0.75* var(--default-padding));
}
</style>