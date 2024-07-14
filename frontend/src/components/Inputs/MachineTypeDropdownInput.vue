<script setup>
import { ref, computed } from 'vue';
import { useTechnologiesStore } from '@/stores/technologies';
import { useMachinesStore } from '@/stores/machines';

import InputLabel from '../BaseInputs/InputLabel.vue';
import InputError from '../BaseInputs/InputError.vue';
import InputDropdownHeader from '../BaseInputs/InputDropdownHeader.vue';
import InputDropdownOptionList from '../BaseInputs/InputDropdownOptionList.vue';

const props = defineProps({
    id: {
        type: String,
        default: "machine-type-dropdown",
    },
    preset: {
        type: String,
        default: "",
    },
    error: String,
})

const areOptionsShown = ref(false);
const value = ref(props.preset);
let name = "Maschinentypen"

const machinesStore = useMachinesStore();
const filteredMachines = computed(() => {
    if (!value.value) {
        return machinesStore.machine_types
    }
    return machinesStore.machine_types.filter((machine_type) => machine_type.includes(value.value))
})

const optionClicked = (option) => {
    value.value = option
}
const toggleOptions = () => {
    areOptionsShown.value = !areOptionsShown.value
}
</script>

<template>
    <InputLabel 
        :id=id
        :name=name />
    <InputDropdownHeader 
        :id="id"
        :name="name"
        :is-changeable="false"
        v-model:value="value"
        @toggle="toggleOptions" />
    <div v-show="areOptionsShown" ><!-- div is needed for the v-show here -->
        <InputDropdownOptionList 
            :base-id="id"
            :deleteable="false"
            :filtered-options="filteredMachines"
            @selected="optionClicked" />
    </div>
    <InputError :error="error" />
</template>

<style scoped>
</style>
