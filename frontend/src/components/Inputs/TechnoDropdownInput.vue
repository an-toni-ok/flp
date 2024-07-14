<script setup>
import { ref } from 'vue';
import { useTechnologiesStore } from '@/stores/technologies';

import TechnologiesList from './TechnologiesList.vue';
import InputLabel from './InputLabel.vue';
import IconButton from './IconButton.vue';
import InputError from './InputError.vue';

import IconPlus from '../icons/IconPlus.vue';
import IconArrowDown from '../icons/IconArrowDown.vue';

const props = defineProps({
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

const isFocused = ref(false);
const areOptionsShown = ref(false);
const value = ref(props.preset);
let name = "Technologie"

const technologiesStore = useTechnologiesStore()

const handleFocus = () => {
    isFocused.value = true
}
const handleBlur = () => {
    isFocused.value = false
}
const optionClicked = (option) => {
    value.value = option
}
const toggleOptions = () => {
    areOptionsShown.value = !areOptionsShown.value
    isFocused.value = true
}
</script>

<template>
    <InputLabel 
        :is-focused="isFocused"
        :name=name
        :id=name />
    <div class="dropdown-input">
        <input 
            @focus="handleFocus" 
            @blur="handleBlur" 
            :class="{'focus': isFocused, 'not-changeable': !isChangeable }"
            class="input-field"
            type="text" 
            :name="name" 
            :id="name" 
            v-model="value" >
        <IconButton 
            v-if="isChangeable"
            @click="technologiesStore.add(value)"
            @focus="handleFocus" 
            @blur="handleBlur" 
            :is-focused="isFocused"
            help_text="Save the technology.">
            <IconPlus />
        </IconButton>
        <IconButton
            @click="toggleOptions"
            @focus="handleFocus"
            @blur="handleBlur"
            :is-focused="isFocused"
            help_text="Toggle a list of currently set technology options.">
            <IconArrowDown />
        </IconButton>
    </div>
    <div v-show="areOptionsShown" >
        <TechnologiesList 
            :is-focused="false"
            :deleteable="areTechnologiesDeleteable"
            @selected="optionClicked" />
    </div>
    <InputError :error="error" />
</template>

<style scoped>
.dropdown-input {
    display: flex;
}

.input-field {
    box-sizing: border-box;
    height: 30px;
    border: 1px solid var(--color-border);
    margin: 0;
    padding: 0;
    background-color: var(--color-background);
    text-align: right;
    padding-right: 10px;
    width: 150px;
    font-size: var(--font-size);
}

.input-field:focus {
    outline: none;
}

.not-changeable {
    width: 180px;
}

.focus {
    border-color: var(--color-text-primary);
    color: var(--color-text-primary);
}
</style>
