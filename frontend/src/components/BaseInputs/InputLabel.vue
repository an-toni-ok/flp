<script setup>
const props = defineProps({
    name: {
        type: String,
        required: true,
    },
    id: {
        type: String,
        required: true,
    }
})
</script>

<template>
    <label 
        class="input-label"
        :for="id">
        {{ name }}
    </label>
</template>

<style scoped>
.input-label {
    padding-left: 8px;
    color: var(--color-text-secondary)
}
</style>