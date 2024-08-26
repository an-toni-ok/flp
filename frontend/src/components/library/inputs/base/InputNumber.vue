<script setup>
const props = defineProps({
    name: {
        type: String,
        required: true
    },
    id: {
        type: String,
        required: true
    },
})

// Model: https://vuejs.org/guide/components/v-model.html
const input_value = defineModel('value', { required: true }) 
</script>

<template>
    <input 
        class="text-input"
        type="number" 
        :name="name" 
        :id="id"
        v-model="input_value">
</template>

<style scoped>
/** 
The base styling for HTML components like 
inputs is in src/assets/main.css. 
*/
</style>