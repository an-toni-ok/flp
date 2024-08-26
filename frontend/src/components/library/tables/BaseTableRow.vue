<script setup>
const props = defineProps({
    show_actions: {
        type: Boolean,
        default: true,
    },
    is_data: {
        type: Boolean,
        default: true
    }
})
</script>

<template>
    <tr>
        <slot></slot>
    </tr>
</template>

<style scoped>
tr > :deep(td),
tr > :deep(th) {
    padding: 0.75rem 0.625rem;
    text-align: center;
}

tr > :deep(.reduce-height) {
    padding-block: 0.25rem;
}

tr > :deep(td:first-child),
tr > :deep(th:first-child) {
    padding-left: 1rem;
}
tr > :deep(td:last-child),
tr > :deep(th:last-child) {
    padding-right: 1rem;
}

tr > :deep(th) {
    font-weight: 700;
}
</style>