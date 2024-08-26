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
        <template v-slot:data>
            <td>{{ machine.name }}</td>
            <td>{{ machine.hourly_rate }}</td>
            <td>{{ machine.investment_cost }}</td>
            <td>{{ machine.additional_machine_time }}</td>
            <td>{{ machine.x_dimension }}</td>
            <td>{{ machine.y_dimension }}</td>
        </template>
        <template v-slot:tech>
            <ExpandableText 
                help_text="Show all technologies"
                :text="machine.technologies.join(', ')" />
        </template>
        <template v-slot:actions>
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
        </template>
    </BaseTableRow>
</template>

<style scoped>
</style>