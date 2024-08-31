<script setup>
import { IconArrowsRight } from '@/components/icons';
import { IconButton } from '@/components/library/buttons';
import { computed } from 'vue';

const props = defineProps({
    title: {
        type: String,
        required: true
    }
})

const opened = defineModel('opened', { required: true })
const text = computed(() => {
    return opened.value ? 'Schließen' : 'Öffnen'
})
</script>

<template>
    <div class="overlay">
        <div :class="[
            'toggle-icon', 
            opened ? '' : 'toggle-icon-closed'
            ]">
            <IconButton 
                :text="text" 
                tooltip-position="left" 
                :borders="false"
                @click="opened = !opened">
                <IconArrowsRight />
            </IconButton>
        </div>
        <div :class="['data', opened ? 'data-open' : 'data-closed']">
            <h2 class="overlay-title">{{ title }}</h2>
            <div v-if="opened">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<style scoped>
.overlay {
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 2rem 0.5rem;
    border-left: 1px solid var(--color-border);
    background-color: var(--color-background);
    /* Make sure the overlay is over the edit button when it's focused. */
    z-index: 2; 
}

.toggle-icon {
    min-width: 2.5rem;
    height: 2.5rem;
    position: relative;
}

.toggle-icon > :deep(button) {
    position: absolute;
    top: 0;
    right: 0;
}

.toggle-icon > :deep(button > div > svg) {
    transition: rotate 0.3s ease;
}

.toggle-icon-closed > :deep(button > div > svg) {
    rotate: 180deg;
    transition: rotate 0.3s ease;
}

.data {
    height: 100%;
    display: flex;
}

.data-closed {
    align-items: flex-end;
    justify-content: center;
}

.data-open {
    padding: 0 3rem;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    gap: 2rem;
}

.overlay-title {
    font-size: var(--font-size-h2);
    line-height: 1;
    white-space: nowrap;
    overflow-x: clip;
}

.data-closed > .overlay-title {
    writing-mode: vertical-lr;
    transform: rotate(180deg);
}
</style>