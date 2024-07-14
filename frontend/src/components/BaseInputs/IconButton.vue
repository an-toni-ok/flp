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
    hasBorderTop: {
        type: Boolean,
        default: true
    },
    hasBorderLeft: {
        type: Boolean,
        default: false
    }
})

defineEmits(['click', 'focus', 'blur']);
</script>

<template>
    <button
        @click="$emit('click')"
        class="icon-button" 
        :class="{ 
            'focus': isFocused, 
            'no-top': !hasBorderTop, 
            'no-left': !hasBorderLeft 
        }"
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
    width: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.icon-button > * {
    width: 15px;
    height: 15px;
}

.no-top {
    margin-top: -1px;
}

.no-left {
    margin-left: -1px;
}
</style>
