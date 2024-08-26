<script setup>
import { InputLabel, InputError, InputText } from './base';

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
</script>

<template>
    <div class="number-input">
        <InputLabel 
            :name="name"
            :id="id" />
        <div class="custom-string-input">
            <InputText 
                :name="name"
                :id="id" 
                v-model:value="value" />
        </div>
        <InputError :error="error" />
    </div>
</template>

<style scoped>
.custom-string-input {
    display: flex;
    /** InputNumber will take all of the space remaining. */
    width: var(--input-width);
}
</style>
