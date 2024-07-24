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
    show_actions: {
        type: Boolean,
        default: true
    }
})
</script>

<template>
    <tr>
        <td>{{ technology }}</td>
        <td>{{ machine_time }}</td>
        <td>{{ manual_time }}</td>
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

tr > td:first-child {
    max-width: 60ch;
    word-wrap: break-word;
}

tr > td:nth-child(2), 
tr > td:nth-child(3) {
    text-align: center;
}
</style>