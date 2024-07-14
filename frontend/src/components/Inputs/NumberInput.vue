<script setup>
import { ref } from 'vue';
import IconButton from './IconButton.vue';
import InputLabel from '../BaseInputs/InputLabel.vue';
import InputError from '../BaseInputs/InputError.vue';

import IconPlus from '../icons/IconPlus.vue';
import IconMinus from '../icons/IconMinus.vue';

const props = defineProps({
    name: {
        type: String,
        required: true,
    },
    preset: {
        type: Number,
        default: 0,
    },
    error: String
})

const value = ref(props.preset);
const isFocused = ref(false)

const add = () => {
    value.value += 1;
}
const subtract = () => {
    value.value -= 1;
}
const handleFocus = () => {
    isFocused.value = true
}
const handleBlur = () => {
    isFocused.value = false
}
</script>

<template>
    <div class="number-input">
        <InputLabel 
            :is-focused="isFocused"
            :name="name"
            :id="name" />
        <div class="custom-number-input">
            <input 
                @focus="handleFocus" 
                @blur="handleBlur" 
                :class="isFocused ? 'focus' : ''"
                class="input-field"
                type="number" 
                :name="name" 
                :id="name" 
                v-model="value" >
            <IconButton 
                @click="add()"
                @focus="handleFocus" 
                @blur="handleBlur"
                :is-focused="isFocused"
                :help_text="'Increment the number input ' + name + ' by one'" >
                <IconPlus />
            </IconButton>
            <IconButton 
                @click="subtract()"
                @focus="handleFocus" 
                @blur="handleBlur"
                :is-focused="isFocused"
                :help_text="'Increment the number input ' + name + ' by one'" >
                <IconMinus />
            </IconButton>
        </div>
        <InputError :error="error" />
    </div>
</template>

<style scoped>
.input-label {
    padding-left: 8px;
    color: var(--color-text-secondary)
}

.custom-number-input {
    display: flex;
}

/* Remove standart mini buttons*/
input[type="number"] {
  -webkit-appearance: textfield;
     -moz-appearance: textfield;
          appearance: textfield;
}
input[type=number]::-webkit-inner-spin-button, 
input[type=number]::-webkit-outer-spin-button { 
  -webkit-appearance: none;
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
}

.input-field:focus {
    outline: none;
}

.focus {
    border-color: var(--color-text-primary);
    color: var(--color-text-primary);
}
</style>
