<script setup>
const props = defineProps({
    help_text: {
        type: String,
        required: true
    },
    focus: {
        type: Boolean,
        default: true,
    }
})

defineEmits(['click']);
</script>

<template>
    <button
        @click="$emit('click')"
        class="icon-button" 
        :class="{ 'focus': focus }"
        :aria-label="help_text"
        :data-tool-tip="help_text" >
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
    width: fit-content;
    position: relative;
}

.icon-button::after {
    content: attr(data-tool-tip);
    position: absolute;
    background-color: var(--color-background);
    padding: 0.5rem;
    border: 1px solid var(--color-border);
    top: -100%;
    right: 0;
    white-space: nowrap;
    transform: scale(0);
    z-index: 1;
}

.icon-button:hover::after {
    transform: scale(1);
}

.focus:focus > * {
    fill: var(--color-brand);
}

.icon-button > * {
    width: 1rem;
}
</style>
