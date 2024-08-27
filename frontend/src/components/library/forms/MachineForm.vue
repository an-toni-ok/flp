<script setup>
import { ref } from 'vue';
import { useMachinesStore } from '@/stores/machines';
import { NumberInput, StringInput, TechnologyDropdownInput } from '@/components/library/inputs';
import { InputOptionList } from '@/components/library/inputs/base';
import { TextButton } from '@/components/library/buttons';

const props = defineProps({
    action_type: {
        type: String,
        default: "erstellen"
    }
})

const machinesStore = useMachinesStore();
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
    <div class="data-layout">
        <div class="data-input-group">
            <h2 class="input-subheading">Grunddaten</h2>
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
        <div class="data-input-group">
            <h2 class="input-subheading">Daten</h2>
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
        <div class="technologies">
            <h2 class="input-subheading">Technologien</h2>
            <div class="split data-input-group">
                <TechnologyDropdownInput 
                    v-model:value="machinesStore.input_technology_value"
                    v-model:options="areOptionsShown"
                    :is-changeable="true"
                    :is-deletable="true"
                    :is-multi-input="true"
                    :has-label="false"
                    @set="set_tech" />
                <InputOptionList 
                    v-if="machinesStore.input_set_technologies.length > 0"
                    base-id="chosen-tech-"
                    :deleteable="true"
                    :filtered-options="machinesStore.input_set_technologies"
                    @delete="del_tech" />
            </div>
        </div>
        <div class="overlay-input-button">
            <TextButton 
                @click="machinesStore.set"
                :text="action_type"/>
        </div>
    </div>
</template>

<style scoped>
.data-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    padding: 2rem;
    border: 1px solid var(--color-border);
}

.technologies {
    grid-column: span 2;
}

.data-input-group > :not(h2) {
    margin-bottom: 0.5rem;
}

.split {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
}

.overlay-input-button {
    grid-column: span 2;
    justify-self: end;
}

.input-subheading {
    font-size: var(--font-size-h3);
    margin-bottom: 1rem;
}
</style>