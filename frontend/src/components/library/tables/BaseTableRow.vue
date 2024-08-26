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
        <!-- <slot name="data"></slot>
        <td class="technologies">
            <slot name="tech"></slot>
        </td>
        <td v-if="show_actions" class="actions">
            <div class="center">
                <slot name="actions"></slot>
            </div>
        </td> -->
    </tr>
</template>

<style scoped>
tr > :deep(td),
tr > :deep(th) {
    padding: 0.75rem 0.5rem;
    text-align: center;
}

tr > :deep(.reduce-height) {
    padding-block: 0.25rem;
}

tr > :deep(td:first-child),
tr > :deep(th:first-child) {
    padding-inline: 1rem;
}

tr > :deep(th) {
    font-weight: 700;
}

.center {
    display: flex;
    justify-content: center;
}
</style>