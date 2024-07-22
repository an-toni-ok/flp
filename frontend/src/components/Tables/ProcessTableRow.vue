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
        <td >
            <slot></slot>
        </td>
    </tr>
</template>

<style scoped>
tr > td:first-child {
    max-width: 60ch;
    word-wrap: break-word;
}

tr > td:nth-child(2), 
tr > td:nth-child(3) {
    text-align: center;
}
</style>