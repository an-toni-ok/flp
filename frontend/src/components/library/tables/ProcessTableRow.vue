<script setup>
import { useProcessesStore } from '@/stores/processes';
import { BaseTableRow } from '@/components/library/tables';
import { IconButton } from '@/components/library/buttons';

import { IconEdit, IconDuplicate, IconDelete, IconMoveDown, IconMoveUp } from '@/components/icons';

const props = defineProps({
    process: {
        required: true,
    },
    index: {
        type: Number,
        required: true
    },
    show_actions: {
        type: Boolean,
        default: true,
    }
})

const processesStore = useProcessesStore();
</script>

<template>
    <BaseTableRow :show_actions="show_actions">
        <td>{{ process.technology }}</td>
        <td>{{ process.machine_time }}</td>
        <td>{{ process.manual_time }}</td>
        <td v-if="show_actions" class="reduce-height">
            <div class="center">
                <IconButton 
                    text="Bearbeiten"
                    :borders="false"
                    tooltip-position="top"
                    @click="processesStore.edit(index)">
                    <IconEdit />
                </IconButton>
                <IconButton
                    text="Nach oben verschieben"
                    :borders="false"
                    tooltip-position="top"
                    @click="processesStore.move(index, false)">
                    <IconMoveDown />
                </IconButton>
                <IconButton
                    text="Nach unten verschieben"
                    :borders="false"
                    tooltip-position="top"
                    @click="processesStore.move(index, true)">
                    <IconMoveUp />
                </IconButton>
                <IconButton
                    text="Duplizieren"
                    :borders="false"
                    tooltip-position="top"
                    @click="processesStore.clone(index)">
                    <IconDuplicate />
                </IconButton>
                <IconButton
                    text="Löschen"
                    :borders="false"
                    tooltip-position="top"
                    @click="processesStore.del(index)">
                    <IconDelete />
                </IconButton>
            </div>
        </td>
    </BaseTableRow>
</template>

<style scoped>
.center {
    display: flex;
    justify-content: center;
}
</style>