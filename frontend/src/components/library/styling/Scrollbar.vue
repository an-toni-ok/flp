<!-- 
This component can be used to wrap another component
with a scrollbar.

Note:
It will set the bottom border to have a border shown
at the bottom regardless of the activation of the
scrollbar.
-->
<script setup>
const props = defineProps({
    scrollStart: {
        type: String,
        default: "100vh"
    }
})
</script>

<template>
    <div class="scrollbar" :style="{ maxHeight: scrollStart }">
        <slot></slot>
    </div>
</template>

<style scoped>
.scrollbar {
    --scrollbar-width: 6px;
    overflow-y: auto;
    overflow-x: hidden;
    width: fit-content;
    border-bottom: 1px solid var(--color-border);
}

.scrollbar::-webkit-scrollbar {
    width: var(--scrollbar-width);
    border-right: 1px solid var(--color-border);
}

.scrollbar::-webkit-scrollbar-thumb {
    width: var(--scrollbar-width);
    border-radius: 50px;
    background-color: var(--color-border);
}
</style>