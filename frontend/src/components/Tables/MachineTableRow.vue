<script setup>
const props = defineProps({
    machine: {
        required: true,
    },
})
</script>

<template>
    <tr>
        <td>{{ machine.machine_type  }}</td>
        <td>{{ machine.machine_hourly_cost }}</td>
        <td>{{ machine.investion_cost }}</td>
        <td>{{ machine.additional_machine_time }}</td>
        <td>{{ machine.breite }}</td>
        <td>{{ machine.laenge }}</td>
        <td>{{ machine.set_technologies }}</td>
        <td class="action">
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

tr > td:first-child {
    max-width: 60ch;
    word-wrap: break-word;
}

tr > td:nth-child(2), 
tr > td:nth-child(3) {
    text-align: center;
}
</style>