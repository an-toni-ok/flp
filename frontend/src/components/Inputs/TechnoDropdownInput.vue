<script setup>
import { ref, computed } from 'vue';
import { useTechnologiesStore } from '@/stores/technologies';

import InputLabel from '../BaseInputs/InputLabel.vue';
import InputError from '../BaseInputs/InputError.vue';
import InputDropdownHeader from '../BaseInputs/InputDropdownHeader.vue';
import InputDropdownOptionList from '../BaseInputs/InputDropdownOptionList.vue';

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
const addHandler = (value) => {
    if (props.isChangeable) {
        technologiesStore.add(value)
    }
}
const deleteHandler = (value) => {
    technologiesStore.remove(value)
}
</script>

<template>
    <InputLabel 
        :id=id
        :name=name />
    <InputDropdownHeader 
        :id="id"
        :name="name"
        :is-changeable="props.isChangeable"
        v-model:value="value"
        @add="addHandler"
        @toggle="toggleOptions" />
    <div v-show="areOptionsShown" ><!-- div is needed for the v-show here -->
        <InputDropdownOptionList 
            :base-id="id"
            :deleteable="areTechnologiesDeleteable"
            :filtered-options="filteredTechnologies"
            @selected="optionClicked"
            @delete="deleteHandler" />
    </div>
    <InputError :error="error" />
</template>

<style scoped>
</style>
