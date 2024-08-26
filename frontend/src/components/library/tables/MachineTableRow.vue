<script setup>
import { useMachinesStore } from '@/stores/machines';
import { ExpandableText } from '@/components/library/util';
import { BaseTableRow } from '@/components/library/tables';
import { IconButton } from '@/components/library/buttons';

import { IconEdit, IconDuplicate, IconDelete } from '@/components/icons';

const props = defineProps({
    machine: {
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

const machinesStore = useMachinesStore();
</script>

<template>
    <BaseTableRow :show_actions="show_actions">
        <td>{{ machine.name }}</td>
        <td>{{ machine.hourly_rate }}</td>
        <td>{{ machine.investment_cost }}</td>
        <td>{{ machine.additional_machine_time }}</td>
        <td>{{ machine.x_dimension }}</td>
        <td>{{ machine.y_dimension }}</td>
        <td class="reduce-height">
            <ExpandableText 
                help_text="Show all technologies"
                :text="machine.technologies.join(', ')" />
        </td>
        <td v-if="show_actions" class="reduce-height">
            <div class="center">
                <IconButton 
                    text="Bearbeiten"
                    :borders="false"
                    tooltip-position="top"
                    @click="machinesStore.edit(index)">
                    <IconEdit />
                </IconButton>
                <IconButton
                    text="Duplizieren"
                    :borders="false"
                    tooltip-position="top"
                    @click="machinesStore.clone(index)">
                    <IconDuplicate />
                </IconButton>
                <IconButton
                    text="Löschen"
                    :borders="false"
                    tooltip-position="top"
                    @click="machinesStore.del(index)">
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