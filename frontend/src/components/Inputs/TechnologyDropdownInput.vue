<script setup>
import { ref, computed } from 'vue';
import { useTechnologiesStore } from '@/stores/technologies';

import InputDropdownHeader from '../BaseInputs/InputDropdownHeader.vue';
import InputDropdownOptionList from '../BaseInputs/InputOptionList.vue';
import InputDropdown from '../BaseInputs/InputDropdown.vue';

const props = defineProps({
    id: {
        type: String,
        default: "technology-dropdown",
    },
    isChangeable: {
        type: Boolean,
        default: false,
    },
    isDeletable: {
        type: Boolean,
        default: false,
    },
    isMultiInput: {
        type: Boolean,
        default: false,
    },
    hasLabel: {
        type: Boolean,
        default: true
    },
    error: String,
})

const emit = defineEmits(['set'])

// Model: https://vuejs.org/guide/components/v-model.html
const value = defineModel('value', { required: true }) 
// Model: https://vuejs.org/guide/components/v-model.html
const areOptionsShown = defineModel('options', { default: false }) 

let name = "Technologie"

const technologiesStore = useTechnologiesStore();
const filteredTechnologies = computed(() => {
    if (!value.value) {
      return technologiesStore.technologies
    }
    return technologiesStore.technologies.filter((tech) => tech.includes(value.value))
})

const optionClicked = (option) => {
    value.value = option
}
const toggleOptions = () => {
    areOptionsShown.value = !areOptionsShown.value
}
const addHandler = (current_value) => {
    if (props.isChangeable) {
        technologiesStore.add(current_value)
    }
    if (props.isMultiInput) {
        emit('set', current_value)
        value.value = ""
    }
}
const deleteHandler = (value) => {
    technologiesStore.remove(value)
}
</script>

<template>
    <InputDropdown 
        :id="id"
        :name="name"
        :are-options-shown="areOptionsShown"
        :error="error"
        :has-label="hasLabel" >
        <template v-slot:header>
            <InputDropdownHeader 
                :id="id"
                :name="name"
                :is-changeable="props.isChangeable"
                v-model:value="value"
                @add="addHandler"
                @toggle="toggleOptions" />
        </template>
        <template v-slot:options>
            <InputDropdownOptionList 
                :base-id="id"
                :deleteable="isDeletable"
                :filtered-options="filteredTechnologies"
                @selected="optionClicked"
                @delete="deleteHandler" />
        </template>
    </InputDropdown>
</template>

<style scoped>
</style>
