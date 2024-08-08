<script setup>
const props = defineProps({
    title: {
        type: String,
        required: true
    },
    textArray: {
        type: Array[String],
        required: true
    }
})
</script>

<template>
    <div class="text-site">
        <h1 class="page-title">{{ title }}</h1>
        <p v-for="text in textArray" class="page-text">{{ text }}</p>
    </div>
</template>

<style scoped>
.text-site {
    margin: var(--site-margin-tb) auto;
    max-width: 80ch;
}

.page-title {
    font-size: var(--font-size-h1);
    margin-bottom: 1.5rem;
}

.page-text {
    margin-bottom: 1.25rem;
}
</style>