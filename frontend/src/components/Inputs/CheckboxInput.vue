<script setup>
import IconConfirm from '../icons/IconConfirm.vue';

const props = defineProps({
    id: {
        type: String,
        required: true
    },
    name: {
        type: String,
        required: true,
    },
});

// Model: https://vuejs.org/guide/components/v-model.html
const checked = defineModel('value', { required: true }) 
</script>

<template>
    <label :for="id" class="checkbox-input">
        <div class="fake-checkbox" aria-hidden="true">
            <IconConfirm v-show="checked" />
        </div>
        <input 
            type="checkbox" 
            :id="id" 
            :name="name"
            v-model="checked"
            class="hidden-visually" >
        {{ name }}
    </label>
</template>

<style scoped>
/** 
The base styling for HTML components like 
inputs is in src/assets/main.css. 
*/

.checkbox-input {
    height: var(--input-height);
    width: var(--input-width);
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 1rem;
}

.fake-checkbox {
    height: calc(1rem * 1.5);
    width: calc(1rem * 1.5);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--color-border);
    gap: 1rem;
}

.fake-checkbox > * {
    width: 15px;
    height: 15px;
}
</style>