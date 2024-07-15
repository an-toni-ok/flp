<script setup>
const props = defineProps({
    help_text: {
        type: String,
        required: true
    },
    overlapTopBorder: {
        type: Boolean,
        default: false
    },
    overlapLeftBorder: {
        type: Boolean,
        default: true
    }
})

defineEmits(['click']);
</script>

<template>
    <button
        @click="$emit('click')"
        class="icon-button" 
        :class="{ 'no-top': overlapTopBorder, 'no-left': overlapLeftBorder }"
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
    --icon-height: calc(var(--font-size-h2) * 0.725);
    width: var(--icon-height);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    border: none;
}

.icon-button > * {
    width: var(--icon-height);
    height: var(--icon-height);
}

.no-top {
    margin-top: -1px;
}

.no-left {
    margin-left: -1px;
}
</style>
