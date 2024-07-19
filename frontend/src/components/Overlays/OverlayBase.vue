<script setup>
import { ref } from 'vue';

import IconArrowsRight from '../icons/IconArrowsRight.vue';
import OverlayIconButton from '../BaseInputs/OverlayIconButton.vue';

const props = defineProps({
    title: {
        type: String,
        required: true
    }
})

const opened = ref(true)
</script>

<template>
    <div class="var-wrapper">
        <div class="overlay" :class="{ 'overlay-closed': !opened }">
            <div class="overlay-header" :class="{ 'close': !opened, 'open': opened }">
                <h1 class="overlay-title">{{ title }}</h1>
                <OverlayIconButton 
                    @click="opened = !opened"
                    help_text="Open/Close the overlay.">
                    <IconArrowsRight />
                </OverlayIconButton>
            </div>
            <div class="min-size-container">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<style scoped>
.var-wrapper {
    --base-padding-width: 1rem;
    --top-padding-width: calc(2 * var(--base-padding-width));
    --overlay-width: var(--font-size-h2);
    --overlay-closed-width: calc(2 * var(--base-padding-width) + var(--overlay-width));
}

.overlay {
    height: 100vh;
    border-left: 1px solid var(--color-border);
    width: fit-content;
    position: fixed;
    top: 0;
    right: 0;
    background-color: var(--color-background);
    padding: 
        var(--top-padding-width)
        var(--top-padding-width)
        var(--top-padding-width)
        calc(3 * var(--base-padding-width));
}

.overlay-header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
    gap: 4rem;
}

.overlay-title {
    font-size: var(--font-size-h2);
    line-height: 1;
    /* transition: transform 0.3s ease, opacity 0.3s ease; */
    white-space: nowrap;
}

.overlay-closed {
    width: var(--overlay-closed-width);
    padding: var(--top-padding-width) var(--base-padding-width);
}

.open {
    height: 9rem;
    align-items: flex-start;
}

.open > .overlay-title {
    align-self: flex-end;
    padding-bottom: 2rem;
}

.close > .overlay-title {
    writing-mode: vertical-lr;
    font-size: var(--font-size-h2);
    transform: rotate(180deg);
}

.close > button > svg {
    transform: rotate(180deg);
}

.close {
    height: 100%;
    width: fit-content;
    flex-direction: column-reverse;
    align-items: center;
}

.min-size-container {
    min-width: 17.842rem;
    padding: 2rem;
    border: 1px solid var(--color-border)
}

.overlay-closed > .min-size-container {
    display: none;
}
</style>