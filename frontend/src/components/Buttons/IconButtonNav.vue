<script setup>
const props = defineProps({
    help_text: {
        type: String,
        required: true
    }
})

defineEmits(['click']);
</script>

<template>
    <button
        @click="$emit('click')"
        class="icon-button" 
        :aria-label="help_text" >
        <slot></slot>
    </button>
</template>

<style scoped>
/** 
The base styling for HTML components like 
buttons is in src/assets/main.css. 
*/
.icon-button {
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
}

.icon-button:focus > * {
    fill: var(--color-brand);
}

.icon-button > * {
    width: 1rem;
}
</style>
