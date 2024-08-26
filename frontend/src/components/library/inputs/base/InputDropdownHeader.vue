<script setup>
import { InputText } from '@/components/library/inputs/base';
import { IconButton } from '@/components/library/buttons';

import { IconPlus, IconArrowDown } from '@/components/icons';

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
            :small="true"
            tooltipPosition="top"
            text="Wert speichern">
            <IconPlus />
        </IconButton>
        <IconButton
            @click="$emit('toggle')"
            :small="true"
            tooltipPosition="top"
            text="Werteliste anzeigen">
            <IconArrowDown />
        </IconButton>
    </div>
</template>

<style scoped>
.dropdown-input {
    display: flex;
    width: var(--input-width);
}

.dropdown-input > *:not(:first-child) {
    margin-left: -1px;
}
</style>