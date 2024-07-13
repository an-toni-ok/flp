<script setup>
const props = defineProps({
    help_text: {
        type: String,
        required: true
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
        :aria-label="help_text" >
        <slot></slot>
    </button>
</template>

<style scoped>
.input-button {
    border-left: none;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--color-border);
    box-sizing: border-box;
    background-color: var(--color-background);
}

.input-button > svg {
    width: 15px;
}
</style>
