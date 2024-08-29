<script setup>
import { InputHeading } from '@/components/library/heading';
import { ProgressButton } from '@/components/library/buttons';
import { IconsDisplay, ZoomDisplay } from '@/components/library/toolbar';

defineEmits(['next'])
</script>

<template>
    <div class="actions-container">
        <div class="tool-area">
            <InputHeading 
                title="Flächeneingabe" 
                nr="1"
                max="4" />
            <IconsDisplay />
            <ZoomDisplay />
        </div>
        <ProgressButton 
            @next="$emit('next')"
            @prev="" />
    </div>
</template>

<style scoped>
.actions-container {
    position: relative;
    padding-block: var(--site-margin-tb);
    padding-inline: var(--site-margin-lr);
    flex: 1;
    height: 100%;
    display: flex;
    flex-direction: column-reverse;
    justify-content: space-between;
}

.tool-area {
    z-index: 3;
    position: absolute;
    top: var(--site-margin-tb);
    left: var(--site-margin-lr);
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 2rem;
}
</style>
