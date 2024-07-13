<script setup>
import { ref } from 'vue';

const props = defineProps({
    name: {
        type: String,
        required: true,
    },
    preset: {
        type: Number,
        default: 0,
    }
})

const value = ref(props.preset);

const add = () => {
    value.value += 1;
}
const subtract = () => {
    value.value -= 1;
}
</script>

<template>
    <label 
        class="input-label"
        :for="name">
        {{ name }}
    </label>
    <div class="custom-number-input">
        <input 
            class="input-field" 
            type="number" 
            :name="name" 
            :id="name" 
            v-model="value" >
        <input 
            @click="add()"
            class="input-button" 
            type="button" 
            value="+"
            :aria-label="'Increment the number input ' + name + ' by one'" >
        <input 
            @click="subtract()"
            class="input-button" 
            type="button" 
            value="-"
            :aria-label="'Decrement the number input ' + name + ' by one'" >
    </div>
</template>

<style scoped>
.movement {
    margin-top: 20px;
    margin-left: 20px;
}

.input-label {
    padding-left: 8px;
    color: var(--color-text-secondary)
}

input {
    height: 30px;
    border: 1px solid var(--color-border);
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    background-color: var(--color-background);
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
    text-align: right;
    padding-right: 10px;
    width: 150px;
}

.input-button {
    border-left: none;
    width: 30px;
}
</style>
