<script setup>
const props = defineProps({
    error: String
})

</script>

<template>
    <p v-if="error" class="error">{{ error }}</p>
</template>

<style scoped>
.error {
    margin: 5px 0;
    padding: 5px 8px 0 8px;
    width: 210px;
    line-height: 1.2;
    color: var(--color-error)
}
</style>