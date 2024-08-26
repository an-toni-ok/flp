<script setup>
import { InputLabel, InputNumber, InputError } from './base';
import { IconButton } from '@/components/library/buttons';

import { IconPlus, IconMinus } from '@/components/icons';

const props = defineProps({
    name: {
        type: String,
        required: true,
    },
    id: {
        type: String,
        required: true
    },
    error: String
})

// Model: https://vuejs.org/guide/components/v-model.html
const value = defineModel('value', { required: true }) 

const add = () => {
    value.value += 1;
}
const subtract = () => {
    value.value -= 1;
}
</script>

<template>
    <div class="number-input">
        <InputLabel 
            :name="name"
            :id="id" />
        <div class="custom-number-input">
            <InputNumber 
                :name="name"
                :id="id" 
                v-model:value="value" />
            <IconButton
                @click="add()"
                :small="true"
                text="Um eins erhöhen" >
                <IconPlus />
            </IconButton>
            <IconButton
                @click="subtract()"
                :small="true"
                text="Um eins verringern" >
                <IconMinus />
            </IconButton>
        </div>
        <InputError :error="error" />
    </div>
</template>

<style scoped>
.custom-number-input {
    display: flex;
    /** InputNumber will take all of the space remaining. */
    width: var(--input-width);
}

.custom-number-input > :not(:first-child) {
    margin-left: -1px;
}
</style>
