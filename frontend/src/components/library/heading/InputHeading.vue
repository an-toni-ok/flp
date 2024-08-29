<script setup>
const props = defineProps({
    title: {
        type: String,
        required: true
    },
    nr: {
        type: Number,
        required: true
    },
    max: {
        type: Number,
        required: true
    }
})
</script>

<template>
    <div class="input-heading">
        <h1>{{ title}}</h1>
        <p><span>{{ nr }}</span> von <span>{{ max }}</span></p>
    </div>
</template>

<style scoped>
.input-heading {
    display: flex;
    align-items: flex-end;
    background-color: var(--color-background);
    border: 1px solid var(--color-border);
    gap: 2rem;
    padding: var(--tool-area-padding) 1.5rem;
    height: 2.5rem;
    width: fit-content;
}

.input-heading > h1 {
    line-height: 1;
    font-size: var(--tool-area-height);
    font-weight: 500;
}

.input-heading > p {
    line-height: 1;
    font-size: 0.8rem;
    text-wrap: nowrap;
}
</style>