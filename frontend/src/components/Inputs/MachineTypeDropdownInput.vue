<script setup>
import { ref, computed } from 'vue';
import { useMachinesStore } from '@/stores/machines';

import InputLabel from '../BaseInputs/InputLabel.vue';
import InputError from '../BaseInputs/InputError.vue';
import InputDropdownHeader from '../BaseInputs/InputDropdownHeader.vue';
import InputDropdownOptionList from '../BaseInputs/InputDropdownOptionList.vue';
import InputDropdown from '../BaseInputs/InputDropdown.vue';

const props = defineProps({
    id: {
        type: String,
        default: "machine-type-dropdown",
    },
    error: String,
})

// Model: https://vuejs.org/guide/components/v-model.html
const value = defineModel('value', { required: true }) 

const areOptionsShown = ref(false);
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
    <InputDropdown
        :id="id"
        :name="name"
        :are-options-shown="areOptionsShown"
        :error="error">
        <template v-slot:header>
            <InputDropdownHeader 
                :id="id"
                :name="name"
                :is-changeable="false"
                v-model:value="value"
                @toggle="toggleOptions" />            
        </template>
        <template v-slot:options>
            <InputDropdownOptionList 
                :base-id="id"
                :deleteable="false"
                :filtered-options="filteredMachines"
                @selected="optionClicked" />            
        </template>
    </InputDropdown>
</template>

<style scoped>
</style>
