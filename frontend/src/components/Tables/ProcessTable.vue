<script setup>
import { useProcessesStore } from '@/stores/processes';
import ProcessTableRow from './ProcessTableRow.vue';
import IconButtonTable from '@/components/Buttons/IconButtonTable.vue'
import IconEdit from '@/components/icons/IconEdit.vue';
import IconMoveDown from '@/components/icons/IconMoveDown.vue';
import IconMoveUp from '@/components/icons/IconMoveUp.vue';
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

const processesStore = useProcessesStore();
</script>

<template>
    <div class="table-container" :class="{ 'short': short_table }">
        <table>
            <tr>
                <th>Technologie</th>
                <th>Extrazeit<br>Maschine</th>
                <th>Extrazeit<br>Manuell</th>
                <th v-show="show_actions" colspan="5">Aktionen</th>
            </tr>
            <ProcessTableRow 
                v-for="(item, index) in processesStore.processes"
                :machine_time="item.machine_time"
                :manual_time="item.manual_time"
                :technology="item.technology"
                :show_actions="show_actions" >
                    <IconButtonTable 
                        help_text="Bearbeiten"
                        @click="processesStore.edit(index)">
                        <IconEdit />
                    </IconButtonTable>
                    <IconButtonTable 
                        help_text="Nach oben verschieben"
                        :focus="false"
                        @click="processesStore.move(index, false)">
                        <IconMoveDown />
                    </IconButtonTable>
                    <IconButtonTable
                        help_text="Nach unten verschieben"
                        :focus="false"
                        @click="processesStore.move(index, true)">
                        <IconMoveUp />
                    </IconButtonTable>
                    <IconButtonTable
                        help_text="Duplizieren"
                        :focus="false"
                        @click="processesStore.clone(index)">
                        <IconDuplicate />
                    </IconButtonTable>
                    <IconButtonTable
                        help_text="Löschen"
                        :focus="false"
                        @click="processesStore.del(index)">
                        <IconDelete />
                    </IconButtonTable>
            </ProcessTableRow>
        </table>
        <p 
            v-if="!processesStore.processes.length"
            class="no-data">Zur Zeit sind noch keine Daten in der Tabelle.</p>
    </div>
</template>

<style scoped>
.table-container {
    --scrollbar-width: 6px;
    max-height: calc(100vh - 15rem);
    overflow-y: auto;
    overflow-x: hidden;
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

table > tr > th:last-child,
table > tr > th:nth-child(2),
table > tr > th:nth-child(3) {
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