<script setup>
import { computed, ref } from 'vue';
import { useTechnologiesStore } from '@/stores/technologies';
import { useMachinesStore } from '@/stores/machines';

import NumberInput from '../Inputs/NumberInput.vue';
import TechnologyDropdownInput from '../Inputs/TechnologyDropdownInput.vue';
import IconArrowsRight from '../icons/IconArrowsRight.vue';
import OverlayIconButton from '../BaseInputs/OverlayIconButton.vue';import InputOptionList from '../BaseInputs/InputOptionList.vue';
import OverlayButton from '../Buttons/OverlayButton.vue';
import StringInput from '../Inputs/StringInput.vue';

const props = defineProps({
    isCreate: {
        type: Boolean,
        default: true
    }
})

const machinesStore = useMachinesStore();
const actionType = computed(() => {
    if (machinesStore.edit_id == 0 || !!machinesStore.edit_id) {
        return "editieren"
    }
    return "erstellen"
})

const technologyStore = useTechnologiesStore();
const expand = computed(() => {
    let num_1 = areOptionsShown.value ? technologyStore.technologies.length : 0;
    let num_2 = machinesStore.input_set_technologies.length

    return (num_1 + num_2) > 6;
})

const areOptionsShown = ref(false);

const set_tech = (tech) => {
    if (machinesStore.input_set_technologies.includes(tech)) {
        return
    }
    machinesStore.input_set_technologies.push(tech)
}
const del_tech = (tech) => {
    if (!machinesStore.input_set_technologies.includes(tech)) {
      return
    }
    let index = machinesStore.input_set_technologies.indexOf(tech)
    machinesStore.input_set_technologies.splice(index, 1)
}
</script>

<template>
    <div class="var-wrapper">
        <div class="overlay" :class="{ 'overlay-closed': !machinesStore.input_overlay_opened }">
            <div class="overlay-header" :class="{ 'close': !machinesStore.input_overlay_opened, 'open': machinesStore.input_overlay_opened }">
                <h1 class="overlay-title">Maschine {{ actionType }}</h1>
                <OverlayIconButton 
                    @click="machinesStore.input_overlay_opened = !machinesStore.input_overlay_opened"
                    help_text="Open/Close the overlay.">
                    <IconArrowsRight />
                </OverlayIconButton>
            </div>
            <div class="min-size-container">
                <div class="overlay-content" v-show="machinesStore.input_overlay_opened">
                    <div class="overlay-column first-column">
                        <div class="overlay-input-group">
                            <h2>Grunddaten</h2>
                            <div class="scrollbar-padding">
                                <StringInput
                                    name="Name"
                                    id="machine-name"
                                    v-model:value="machinesStore.input_name" />
                                <NumberInput 
                                    name="Breite in m"
                                    id="machine-breite"
                                    v-model:value="machinesStore.input_breite" />
                                <NumberInput 
                                    name="Länge in m"
                                    id="machine-laenge"
                                    v-model:value="machinesStore.input_laenge" />
                            </div>
                        </div>
                        <div class="overlay-input-group">
                            <h2>Daten</h2>
                            <NumberInput 
                                name="Maschinenstundensatz (&#8364;)"
                                id="machine-hourly-rate"
                                v-model:value="machinesStore.input_machine_hourly_cost" />
                            <NumberInput 
                                name="Investionskosten (&#8364;)"
                                id="investion-cost"
                                v-model:value="machinesStore.input_investion_cost" />
                            <NumberInput 
                                name="Zusätzliche Maschinenzeit in s"
                                id="additional-machine-time"
                                v-model:value="machinesStore.input_additional_machine_time" />
                        </div>
                    </div>
                    <div class="overlay-column second-column" >
                        <h2>Technologien</h2>
                        <div class="split"
                        :class="{ 'no-scrollbar': !expand }">
                            <TechnologyDropdownInput 
                                v-model:value="machinesStore.input_technology_value"
                                v-model:options="areOptionsShown"
                                :is-changeable="true"
                                :is-deletable="true"
                                :is-multi-input="true"
                                :has-label="false"
                                @set="set_tech" />
                            <InputOptionList 
                                base-id="chosen-tech-"
                                :deleteable="true"
                                :filtered-options="machinesStore.input_set_technologies"
                                @delete="del_tech" />
                        </div>
                    </div>
                    <div class="overlay-input-button">
                        <OverlayButton 
                            @click="machinesStore.set"
                            :text="actionType"/>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped>
.var-wrapper {
    --base-padding-width: 1rem;
    --top-padding-width: calc(2 * var(--base-padding-width));
    z-index: 4;
}

.overlay {
    height: 100%;
    border-left: 1px solid var(--color-border);
    width: fit-content;
    position: absolute;
    top: 0;
    right: 0;
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

.overlay-content {
    display: flex;
    gap: 1rem;
    flex-direction: column;
}

.overlay-column {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.first-column {
    display: flex;
    flex-direction: row;
    gap: 2.5rem;
}

.second-column {
    gap: 2rem;
}

.overlay-input-group > *,
.overlay-input-tech > div > *,
.scrollbar-padding > *,
.scrollbar-padding > div > * {
    margin: 0 0 0.5rem 0;
}

.split {
    display: flex;
    gap: 2rem;
    justify-content: space-between;
}

.no-scrollbar {
    gap: 2.5rem;
}

.split > .scrollbar-padding {
    margin-right: 9px;
}

.overlay-input-button {
    align-self: flex-end;
    margin-right: 9px;
    margin-top: 1.5rem;
}
</style>