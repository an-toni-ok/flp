<script setup>
import { ref } from 'vue';
import { useTechnologiesStore } from '@/stores/technologies';

import InputLabel from '../BaseInputs/InputLabel.vue';
import InputError from '../BaseInputs/InputError.vue';
import DropdownInputHeader from './DropdownInputHeader.vue';
import TechnologiesList from './TechnologiesList.vue';

const props = defineProps({
    id: {
        type: String,
        default: "technology-dropdown",
    },
    preset: {
        type: String,
        default: "",
    },
    isChangeable: {
        type: Boolean,
        default: false,
    },
    areTechnologiesDeleteable: {
        type: Boolean,
        default: false,
    },
    error: String,
})

const areOptionsShown = ref(false);
const value = ref(props.preset);
let name = "Technologie"

const technologiesStore = useTechnologiesStore()

const optionClicked = (option) => {
    value.value = option
}
const toggleOptions = () => {
    areOptionsShown.value = !areOptionsShown.value
}
const addHandler = (value) => {
    if (props.isChangeable) {
        technologiesStore.add(value)
    }
}
</script>

<template>
    <InputLabel 
        :id=id
        :name=name />
    <DropdownInputHeader 
        :id="id"
        :name="name"
        :is-changeable="props.isChangeable"
        v-model:value="value"
        @add="addHandler"
        @toggle="toggleOptions" />
    <div v-show="areOptionsShown" ><!-- div is needed for the v-show here -->
        <TechnologiesList 
            :base-id="id"
            :deleteable="areTechnologiesDeleteable"
            @selected="optionClicked" />
    </div>
    <InputError :error="error" />
</template>

<style scoped>
</style>
