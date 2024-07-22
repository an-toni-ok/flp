<script setup>
import { computed, ref } from 'vue';
import { useTechnologiesStore } from '@/stores/technologies';

import NumberInput from '../Inputs/NumberInput.vue';
import MachineTypeDropdownInput from '../Inputs/MachineTypeDropdownInput.vue';
import TechnologyDropdownInput from '../Inputs/TechnologyDropdownInput.vue';
import OverlayBase from './OverlayBase.vue';
import InputOptionList from '../BaseInputs/InputOptionList.vue';
import OverlayButton from '../Buttons/OverlayButton.vue';

const props = defineProps({
    isCreate: {
        type: Boolean,
        default: true
    }
})

const opened = ref(true)
const breite = ref(0)
const laenge = ref(0)

const machine_hourly_cost = ref(0)
const investion_cost = ref(0)
const additional_machine_time = ref("")
const machine_type = ref("")

const technology_value = ref("")
const set_technologies = ref([]);

const button_text = props.isCreate ? "Erstellen" : "Bearbeiten";
const technologyStore = useTechnologiesStore();
const expand = computed(() => {
    let num_1 = areOptionsShown.value ? technologyStore.technologies.length : 0;
    let num_2 = set_technologies.value.length

    return (num_1 + num_2) > 6;
})

const areOptionsShown = ref(false);

const set_tech = (tech) => {
    if (set_technologies.value.includes(tech)) {
        return
    }
    set_technologies.value.push(tech)
}
const del_tech = (tech) => {
    if (!set_technologies.value.includes(tech)) {
      return
    }
    let index = set_technologies.value.indexOf(tech)
    set_technologies.value.splice(index, 1)
}
</script>

<template>
    <OverlayBase 
        title="Maschine erstellen"
        v-model:opened="opened">
        <div class="overlay-content" v-show="opened">
            <div class="overlay-content-column first-column">
                <div class="overlay-input-group">
                    <h2>Maße</h2>
                    <div :class="{ 'split': expand }">
                        <div class="scrollbar-padding">
                            <NumberInput 
                                name="Breite"
                                id="machine-breite"
                                v-model:value="breite" />
                        </div>
                        <div class="scrollbar-padding">
                            <NumberInput 
                                name="Länge"
                                id="machine-laenge"
                                v-model:value="laenge" />
                        </div>
                    </div>
                </div>
                <div class="overlay-input-group overlay-input-tech">
                    <h2>Technologien</h2>
                    <div :class="{ 'split': expand }">
                        <InputOptionList 
                            base-id="chosen-tech-"
                            :deleteable="true"
                            :filtered-options="set_technologies"
                            @delete="del_tech" />
                        <TechnologyDropdownInput 
                            v-model:value="technology_value"
                            v-model:options="areOptionsShown"
                            :is-changeable="true"
                            :is-deletable="true"
                            :is-multi-input="true"
                            :has-label="false"
                            @set="set_tech" />
                    </div>
                </div>
            </div>
            <div class="overlay-content-column second-column">
                <div class="overlay-input-group">
                    <h2>Daten</h2>
                    <NumberInput 
                        name="Maschinenstundensatz"
                        id="machine-hourly-rate"
                        v-model:value="machine_hourly_cost" />
                    <NumberInput 
                        name="Investionskosten"
                        id="investion-cost"
                        v-model:value="investion_cost" />
                    <NumberInput 
                        name="Zusätzliche Maschinenzeit"
                        id="additional-machine-time"
                        v-model:value="additional_machine_time" />
                    <MachineTypeDropdownInput 
                        v-model:value="machine_type" />
                </div>
                <div class="overlay-input-group overlay-input-button">
                    <OverlayButton 
                        @click=""
                        :text="button_text"/>
                </div>
            </div>
        </div>
    </OverlayBase>
</template>

<style scoped>
.overlay-content {
    display: flex;
    gap: 2rem;
}

.overlay-content-column {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.first-column {
    padding-bottom: 4rem;
}

.second-column {
    justify-content: space-between;
}

.overlay-input-group > *,
.overlay-input-tech > div > * {
    margin: 0 0 0.5rem 0;
}

.split {
    display: flex;
    gap: 1rem;
    justify-content: flex-start;
}

.split > .scrollbar-padding {
    margin-right: 9px;
}
</style>