<script setup>
const props = defineProps({
    text: {
        type: String,
        required: true
    },
    tooltipPosition: {
        type: String,
        default: 'bottom',
        validator: (value) => ['top', 'bottom', 'left', 'right'].includes(value)
    },
    wide: {
        type: Boolean,
        default: false,
    },
    small: {
        type: Boolean,
        default: false,
    },
    borders: {
        type: Boolean,
        default: true
    }
})

defineEmits(['click']);
</script>

<template>
    <button
        @click="$emit('click')"
        :class="[
            'icon-button',
            borders ? 'icon-button-borders' : '',
            'tooltip-pos-' + tooltipPosition, 
            wide ? 'icon-button-wide' : '',
            small ? 'icon-button-small' : ''
        ]"
        :aria-label="text"
        :data-tool-tip="text" >
        <div class="icon-wrapper">
            <slot></slot>

        </div>
    </button>
</template>

<style scoped>
/** 
The base styling for HTML components like 
buttons is in src/assets/main.css. 
*/
.icon-button {
    position: relative;
    display: flex;
    background-color: var(--color-background);
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    padding: 0.75rem;
    border: none;
}

.icon-button-borders {
    border: 1px solid var(--color-border);
}

.icon-wrapper > :deep(svg) {
    width: 1rem;
    height: 1rem;
}

.icon-button-wide {
    width: 8.5rem;
}

.icon-button-wide > .icon-wrapper {
    width: 7rem;
    display: flex;
    justify-content: flex-end;
}

.icon-button-small {
    width: 2rem;
    height: 2rem;
    padding: 0.5rem;
}

.icon-button-small > .icon-wrapper > :deep(svg) {
    width: 0.875rem;
    height: 0.875rem;
}

.icon-button:focus {
    outline: none;
    color: var(--color-text-primary);
    z-index: 1;
}

.icon-button-borders:focus {
    border-color: var(--color-text-primary);
}

.icon-button::after {
    content: attr(data-tool-tip);
    position: absolute;
    background-color: var(--color-background);
    padding: 0.5rem;
    border: 1px solid var(--color-border);
    white-space: nowrap;
    transform: scale(0);
    z-index: 2;
}

.icon-button:hover::after {
    transform: scale(1);
}

.tooltip-pos-top::after {
    bottom: calc(100% + 0.5rem);
}
.tooltip-pos-bottom::after {
    top: calc(100% + 0.5rem);
}
.tooltip-pos-left::after {
    right: calc(100% + 0.5rem);
}
.tooltip-pos-right::after {
    left: calc(100% + 0.5rem);
}
</style>
