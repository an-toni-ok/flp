<script setup>
import { useProcessesStore } from '@/stores/processes';
import ProcessTableRow from './ProcessTableRow.vue';
import IconButtonTable from '@/components/Buttons/IconButtonTable.vue'
import IconEdit from '@/components/icons/IconEdit.vue';
import IconMoveDown from '@/components/icons/IconMoveDown.vue';
import IconMoveUp from '@/components/icons/IconMoveUp.vue';
import IconDuplicate from '@/components/icons/IconDuplicate.vue';
import IconDelete from '@/components/icons/IconDelete.vue';

const processesStore = useProcessesStore();
</script>

<template>
    <div class="table-container">
        <table>
            <tr>
                <th>Technologie</th>
                <th>Extrazeit<br>Maschine</th>
                <th>Extrazeit<br>Manuell</th>
                <th>Aktionen</th>
            </tr>
            <ProcessTableRow 
                v-for="(item, index) in processesStore.processes"
                :machine_time="item.machine_time"
                :manual_time="item.manual_time"
                :technology="item.technology" >
                <td>
                    <IconButtonTable 
                        help_text="Edit this table row"
                        @click="processesStore.edit(index)">
                        <IconEdit />
                    </IconButtonTable>
                </td>
                <td>
                    <IconButtonTable 
                        help_text="Move this table row down"
                        :focus="false"
                        @click="processesStore.move(index, false)">
                        <IconMoveDown />
                    </IconButtonTable>
                </td>
                <td>
                    <IconButtonTable
                        help_text="Move this table row up"
                        :focus="false"
                        @click="processesStore.move(index, true)">
                        <IconMoveUp />
                    </IconButtonTable>
                </td>
                <td>
                    <IconButtonTable
                        help_text="Duplicate this table row"
                        :focus="false"
                        @click="processesStore.clone(index)">
                        <IconDuplicate />
                    </IconButtonTable>
                </td>
                <td>
                    <IconButtonTable
                        help_text="Delete this table row"
                        :focus="false"
                        @click="processesStore.del(index)">
                        <IconDelete />
                    </IconButtonTable>
                </td>
            </ProcessTableRow>
        </table>
        <p 
            v-if="!processesStore.processes.length"
            class="no-data">Zur Zeit sind noch keine Daten in der Tabelle.</p>
    </div>
</template>

<style scoped>
table {
  border-collapse: collapse;
  border-spacing: 0;
  padding-left: 1.5rem;
  min-width: 37rem;
}

table > tr {
    border: 1px solid var(--color-border);
    height: var(--input-height);
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

table > tr > *:last-child {
    padding-right: 1rem;
}

.no-data {
    border: 1px solid var(--color-border);
    border-top: none;
    padding-inline: 1.5rem;
    padding-block: calc(0.75* var(--default-padding));
}
</style>