<script setup>
import { Scrollbar } from '@/components/library/styling';

const props = defineProps({
    scroll_start: {
        type: String,
        default: "20rem"
    },
    empty_text: {
        type: String,
        default: "Zur Zeit sind noch keine Daten in der Tabelle."
    },
    is_empty: {
        type: Boolean,
        default: false,
    }
});

</script>

<template>
    <div class="table-display">
        <Scrollbar :scroll-start="scroll_start">
            <table>
                <slot name="table-head"></slot>
                <slot name="table-rows"></slot>
            </table>
            <p v-if="is_empty" class="empty-text">{{ empty_text }}</p>
        </Scrollbar>
    </div>
</template>

<style scoped>
table {
    border: 1px solid var(--color-border);
    border-bottom: none;
    border-collapse: collapse;
    border-spacing: 0;
    width: 100%;
}

table > :deep(tr:not(:first-child)) {
    border-top: 1px solid var(--color-border);
}

.empty-text {
    border: 1px solid var(--color-border);
    border-bottom: none;
    padding: var(--table-padding);
    text-align: center;
}
</style>