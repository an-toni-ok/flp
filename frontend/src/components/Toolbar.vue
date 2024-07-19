<script setup>
import ZoomDisplay from './Toolbar/ZoomDisplay.vue';
import IconsDisplay from './Toolbar/IconsDisplay.vue';
</script>

<template>
    <div class="tool-area">
        <div class="tool-area-name">
            <h3>Flächeneingabe</h3>
            <p>1/5</p>
        </div>
        <IconsDisplay />
        <ZoomDisplay />
    </div>
</template>

<style scoped>
.tool-area {
    position: absolute;
    top: var(--site-margin-tb);
    left: var(--site-margin-lr);
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 2rem;
}

.tool-area-name {
    display: flex;
    align-items: center;
    background-color: var(--color-background);
    border: 1px solid var(--color-border);
    gap: 2rem;
    padding: var(--tool-area-padding) 1.5rem;
}

.tool-area-name > h3 {
    line-height: 1;
    font-size: var(--tool-area-height);
    font-weight: 500;
}

.tool-area-name > p {
    line-height: 1;
    font-size: 0.8rem;
}
</style>
