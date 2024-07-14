<script setup>
import { computed } from 'vue';

const props = defineProps({
    help_text: {
        type: String,
        required: true
    },
    isFocused: {
        type: Boolean,
        default: false
    },
    withoutTopBorder: {
        type: Boolean,
        default: false
    }
})

defineEmits(['click', 'focus', 'blur']);
</script>

<template>
    <button
        @click="$emit('click')"
        @focus="$emit('focus')" 
        @blur="$emit('blur')"
        class="input-button" 
        :class="{ 'focus': isFocused, 'top-border': withoutTopBorder }"
        :aria-label="help_text" >
        <slot></slot>
    </button>
</template>

<style scoped>
.input-button {
    width: 30px;
    height: 30px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--color-border);
    border-left: none;
    box-sizing: border-box;
    background-color: var(--color-background);
}

.input-button > * {
    width: 15px;
    height: 15px;
}

.focus {
    border-color: var(--color-text-primary);
    color: var(--color-text-primary);
}

.top-border {
    border-top: none;
}
</style>
