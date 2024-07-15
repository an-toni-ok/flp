<script setup>
import { ref } from 'vue';

import IconArrowsRight from '../icons/IconArrowsRight.vue';
import IconButton from '../BaseInputs/IconButton.vue';

const props = defineProps({
    title: {
        type: String,
        required: true
    }
})

const opened = ref(true)
</script>

<template>
    <div class="overlay" :class="{ 'overlay-closed': !opened }">
        <div class="overlay-header" :class="{ 'close': !opened }">
            <h1 class="overlay-title">{{ title }}</h1>
            <IconButton 
                @click="opened = !opened"
                help_text="Open/Close the overlay.">
                <IconArrowsRight />
            </IconButton>
        </div>
        <slot></slot>
    </div>
</template>

<style scoped>
.overlay {
    height: 100vh;
    border-left: 1px solid var(--color-border);
    width: fit-content;
    position: fixed;
    top: 0;
    right: 0;
    padding: 2.5rem 1.5rem 2.5rem 2.5rem;
}

.overlay-header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
    gap: 3rem;
}

.overlay-title {
    line-height: 1;
    /* transition: transform 0.3s ease, opacity 0.3s ease; */
    white-space: nowrap;
}

.overlay-closed {
    width: 5rem;
    padding: 2.5rem 1.5rem;
}

.close > .overlay-title {
    writing-mode: vertical-lr;
    transform: rotate(180deg);
}

.close > button > svg {
    transform: rotate(180deg);
}

.close {
    height: 100%;
    width: fit-content;
    flex-direction: column-reverse;
    align-items: flex-start;
}
</style>