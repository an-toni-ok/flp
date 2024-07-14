<script setup>
import { ref } from 'vue';
import InputLabel from '../BaseInputs/InputLabel.vue';
import InputNumber from '../BaseInputs/InputNumber.vue';
import IconButton from '../BaseInputs/IconButton.vue';
import InputError from '../BaseInputs/InputError.vue';

import IconPlus from '../icons/IconPlus.vue';
import IconMinus from '../icons/IconMinus.vue';

const props = defineProps({
    name: {
        type: String,
        required: true,
    },
    id: {
        type: String,
        required: true
    },
    preset: {
        type: Number,
        default: 0,
    },
    error: String
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
                :help_text="'Increment the number input ' + name + ' by one'" >
                <IconPlus />
            </IconButton>
            <IconButton
                @click="subtract()"
                :help_text="'Increment the number input ' + name + ' by one'" >
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
</style>
