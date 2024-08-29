<script setup>
const props = defineProps({
    text: {
        type: String,
        required: true
    },
    info_name: {
        type: String,
        required: true
    }
})
</script>

<template>
    <div class="stat-display" :data-info="info_name">
        <slot></slot>
        <p>{{ text }}</p>
    </div>
</template>

<style scoped>
.stat-display {
    width: calc(50% - 0.5rem);
    position: relative;
    display: flex;
    height: 1.5rem;
    line-height: 1.5rem;
    align-items: center;
    gap: 0.5rem;
}

.stat-display::after {
    content: attr(data-info);
    z-index: 1;
    right: 0;
    top: 75%;
    position: absolute;
    background-color: var(--color-background);
    padding: 0.5rem;
    border: 1px solid var(--color-border);
    height: 1rem;
    line-height: 1rem;
    transform: scale(0);
}

.stat-display:hover::after {
    transform: scale(1);
}

.stat-display > :deep(svg) {
    height: 1rem;
    width: 1rem;
}
</style>