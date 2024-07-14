<script setup>
import InputText from '../BaseInputs/InputText.vue';
import IconButton from '../BaseInputs/IconButton.vue';

import IconPlus from '../icons/IconPlus.vue';
import IconArrowDown from '../icons/IconArrowDown.vue';

const props = defineProps({
    id: {
        type: String,
        default: "technology-dropdown",
    },
    name: {
        type: String,
        required: true,
    },
    isChangeable: {
        type: Boolean,
        default: false,
    },
})

defineEmits(['add', 'toggle'])

// Model: https://vuejs.org/guide/components/v-model.html
const value = defineModel('value', { required: true }) 
</script>

<template>
    <div class="dropdown-input">
        <InputText 
            :id="id"
            :name="name"
            v-model:value="value"
            @keyup.enter="$emit('add', value)" />
        <IconButton 
            v-if="isChangeable"
            @click="$emit('add', value)"
            help_text="Save the current value.">
            <IconPlus />
        </IconButton>
        <IconButton
            @click="$emit('toggle')"
            help_text="Toggle a list of currently set options.">
            <IconArrowDown />
        </IconButton>
    </div>
</template>

<style scoped>
.dropdown-input {
    display: flex;
    width: var(--input-width);
    position: sticky;
    top: 0;
}
</style>