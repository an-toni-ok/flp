<script setup>
import { Scrollbar } from '@/components/library/styling';

const props = defineProps({
    width: {
        type: String,
        default: "20rem"
    },
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
    <div class="list" :style="{ width: width }">
        <Scrollbar :scroll-start="scroll_start">
            <slot></slot>
            <p class="empty-text" v-if="is_empty">{{ empty_text }}</p>
        </Scrollbar>
    </div>
</template>

<style scoped>
.empty-text {
    border: 1px solid var(--color-border);
    border-bottom: none;
    border-top: none;
    padding: 1rem;
    text-align: center;
}
</style>