<script setup>
import ExpandableText from './ExpandableText.vue';

const props = defineProps({
    machine: {
        required: true,
    },
    show_actions: {
        type: Boolean,
        default: true
    }
})
</script>

<template>
    <tr>
        <td>{{ machine.name }}</td>
        <td>
            <ExpandableText 
                help_text="Show all technologies"
                :text="machine.machine_type" />
        </td>
        <td>{{ machine.machine_hourly_cost }}</td>
        <td>{{ machine.investion_cost }}</td>
        <td>{{ machine.additional_machine_time }}</td>
        <td>{{ machine.breite }}</td>
        <td>{{ machine.laenge }}</td>
        <td>
            <ExpandableText 
                help_text="Show all technologies"
                :text="machine.set_technologies.join(', ')" />
        </td>
        <td v-if="show_actions" class="action">
            <div class="center">
                <slot></slot>
            </div>
        </td>
    </tr>
</template>

<style scoped>
.action {
    white-space: nowrap;
    width: fit-content;
}

.center {
    display: flex;
    justify-content: center;
}

tr > td {
    text-align: right;
}

tr > td:nth-child(1) {
    text-align: left;
    max-width: 30ch;
    word-wrap: break-word;
}
</style>