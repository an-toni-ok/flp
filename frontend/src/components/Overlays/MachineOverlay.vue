<script setup>
import { ref } from 'vue';

import NumberInput from '../Inputs/NumberInput.vue';
import MachineTypeDropdownInput from '../Inputs/MachineTypeDropdownInput.vue';
import TechnologyDropdownInput from '../Inputs/TechnologyDropdownInput.vue';
import OverlayBase from './OverlayBase.vue';
import InputOptionList from '../BaseInputs/InputOptionList.vue';

const opened = ref(true)
const breite = ref(0)
const laenge = ref(0)

const machine_hourly_cost = ref(0)
const investion_cost = ref(0)
const additional_machine_time = ref("")
const machine_type = ref("")

const technology_value = ref("")
const set_technologies = ref([]);
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
    <OverlayBase title="Maschine erstellen">
        <div class="overlay-content" v-show="opened">
            <h2>Maße</h2>
            <NumberInput 
                name="Breite"
                id="machine-breite"
                v-model:value="breite" />
            <NumberInput 
                name="Länge"
                id="machine-laenge"
                v-model:value="laenge" />

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

            <h2>Technologie</h2>
            <TechnologyDropdownInput 
                v-model:value="technology_value"
                :is-changeable="true"
                :is-deletable="true"
                :is-multi-input="true"
                @set="set_tech" />
            <InputOptionList 
                base-id="chosen-tech-"
                :deleteable="true"
                :filtered-options="set_technologies"
                @delete="del_tech" />
        </div>
    </OverlayBase>
</template>

<style scoped>
.overlay-content {
    margin: 2rem 0;
}
.overlay-content > * {
    margin: 1rem 0;
}
</style>