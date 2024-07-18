<script setup>
const props = defineProps({
    text: {
        type: String,
        required: true
    }
})

defineEmits(['click']);
</script>

<template>
    <button
        @click="$emit('click')"
        class="icon-button" >
        {{ text }}
    </button>
</template>

<style scoped>
/** 
The base styling for HTML components like 
buttons is in src/assets/main.css. 
*/
.icon-button {
    width: var(--input-width);
    height: var(--input-height);
    font-size: var(--font-size);
    font-weight: 600;
    padding: 0 calc((var(--input-height) - var(--font-size)) / 2);
    border: 2px solid var(--color-border);
    background-color: var(--color-background);
}

.icon-button:focus > * {
    fill: var(--color-brand);
}

.icon-button > * {
    width: 1rem;
}
</style>
