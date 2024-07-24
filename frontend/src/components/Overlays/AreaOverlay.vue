<script setup>
import { ref } from 'vue';

import NumberInput from '../Inputs/NumberInput.vue';
import OverlayBase from './OverlayBase.vue';
import OverlayButton from '../Buttons/OverlayButton.vue';
import IconArrowsRight from '../icons/IconArrowsRight.vue';
import OverlayIconButton from '../BaseInputs/OverlayIconButton.vue';

const props = defineProps({
    isCreate: {
        type: Boolean,
        default: true
    }
})

const opened = ref(true)

const height = ref(0)
const width = ref(0)
const x_pos = ref(0)
const y_pos = ref(0)

let title = "Fläche erstellen"

const button_text = props.isCreate ? "Erstellen" : "Bearbeiten";
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
                <div class="overlay-content" v-show="opened">
                    <div class="input-split">
                        <h2>Fläche</h2>
                        <NumberInput 
                            name="Breite"
                            id="breite"
                            v-model:value="width" />
                        <NumberInput 
                            name="Höhe"
                            id="hoehe"
                            v-model:value="height" />
                    </div>
                    <div class="input-split">
                        <h2>Position</h2>
                        <NumberInput 
                            name="x-Position"
                            id="x-pos"
                            v-model:value="x_pos" />
                        <NumberInput 
                            name="y-Position"
                            id="y-pos"
                            v-model:value="y_pos" />
                    </div>
                    <OverlayButton 
                        @click=""
                        :text="button_text"/>
                </div>
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
    z-index: 4;
}

.overlay {
    height: 100%;
    border-left: 1px solid var(--color-border);
    width: fit-content;
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

.overlay-content {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.input-split > * {
    margin: 0 0 0.5rem 0;
}

.input-split > h2 {
    font-size: var(--font-size-h3);
}
</style>