<script setup>
const props = defineProps({
    machine_time: {
        type: Number,
        required: true,
    },
    manual_time: {
        type: Number,
        required: true,
    },
    technology: {
        type: String,
        required: true,
    },
})
</script>

<template>
    <tr>
        <td>{{ technology }}</td>
        <td>{{ machine_time }}</td>
        <td>{{ manual_time }}</td>
        <td class="actions">
            <slot></slot>
        </td>
    </tr>
</template>

<style scoped>
.actions {
    display: flex;
}

tr > td:nth-child(2), 
tr > td:nth-child(3) {
    text-align: center;
}
</style>