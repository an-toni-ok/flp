<script setup>
const props = defineProps({
    show_actions: {
        type: Boolean,
        default: true,
    }
})
</script>

<template>
    <tr>
        <slot name="data"></slot>
        <th v-if="show_actions">
            <slot name="action-heading"></slot>
        </th>
    </tr>
</template>

<style scoped>
tr > :deep(td),
tr > :deep(th) {
    padding: 0.75rem 0.5rem;
    text-align: center;
}

.actions, .technologies {
    padding-block: 0.25rem;
}

tr > :deep(td:first-child),
tr > :deep(th:first-child) {
    padding-inline: 1rem;
}

tr > :deep(th) {
    font-weight: 700;
}
</style>