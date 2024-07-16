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
    position: relative;
    --measurement: calc(var(--tool-area-height) +2 * var(--tool-area-padding));
    display: flex;
    align-items: center;
    justify-content: center;
    width: var(--measurement);
    height: var(--measurement);
    padding: var(--tool-area-padding);
    margin-left: -1px;
}

.icon-button > * {
    width: var(--tool-area-height);
    height: var(--tool-area-height);
}
</style>
