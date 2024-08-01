<script setup>
import { useProcessesStore } from '@/stores/processes';
import NumberInput from '../Inputs/NumberInput.vue';
import TechnologyDropdownInput from '../Inputs/TechnologyDropdownInput.vue';
import IconArrowsRight from '../icons/IconArrowsRight.vue';
import OverlayIconButton from '../BaseInputs/OverlayIconButton.vue';import OverlayButton from '../Buttons/OverlayButton.vue';
import { computed } from 'vue';

const props = defineProps({
    isCreate: {
        type: Boolean,
        default: true
    }
})

const processesStore = useProcessesStore();
const actionType = computed(() => {
    if (processesStore.edit_id == 0 || !!processesStore.edit_id) {
        return "editieren"
    }
    return "erstellen"
})
</script>

<template>
    <div class="var-wrapper">
        <div 
            class="overlay" 
            :class="{ 
                'overlay-closed': !processesStore.inputOverlayOpened 
            }" >
            <div 
                class="overlay-header" 
                :class="{ 
                    'close': !processesStore.inputOverlayOpened, 'open': processesStore.inputOverlayOpened 
                }" >
                <h1 class="overlay-title">Prozess {{ actionType }}</h1>
                <OverlayIconButton 
                    @click="processesStore.inputOverlayOpened = !processesStore.inputOverlayOpened"
                    help_text="Open/Close the overlay.">
                    <IconArrowsRight />
                </OverlayIconButton>
            </div>
            <div class="min-size-container">
                <div 
                    class="overlay-content" 
                    v-show="processesStore.inputOverlayOpened">
                    <NumberInput 
                        name="Maschinenzeit"
                        id="machinenzeit"
                        v-model:value="processesStore.input_machine_time" />
                    <NumberInput 
                        name="Manuelle Zeit"
                        id="manual-time"
                        v-model:value="processesStore.input_manual_time" />
                    <TechnologyDropdownInput 
                        v-model:value="processesStore.input_technology"
                        :is-changeable="true"
                        :is-deletable="true" />
                    <OverlayButton 
                        @click="processesStore.set"
                        :text="actionType"/>
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
    /* position: absolute;
    top: 0;
    right: 0; */
    overflow: hidden;
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

.overlay-content > * {
    margin: 0 0 0.5rem 0;

}

.overlay-content > button {
    margin-top: 2rem;
}
</style>