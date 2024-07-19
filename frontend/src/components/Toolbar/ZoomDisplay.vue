<script setup>
import { useToolbarStore } from '@/stores/toolbar';

import ToolIconButton from '@/components/Toolbar/ToolIconButton.vue';
import IconZoomMinus from '@/components/icons/IconZoomMinus.vue';
import IconZoomPlus from '@/components/icons/IconZoomPlus.vue';

const toolbar = useToolbarStore();
</script>

<template>
    <div class="zoom">
        <ToolIconButton 
            help_text="Lower the zoom level."
                @click="toolbar.lowerZoom()" >
            <IconZoomMinus />
        </ToolIconButton>
        <p><span class="zoom-display">{{ toolbar.zoom }}</span> %</p>
        <ToolIconButton 
            help_text="Raise the zoom level."
                @click="toolbar.raiseZoom()" >
            <IconZoomPlus />
        </ToolIconButton>
    </div>
</template>

<style scoped>
.zoom {
    display: flex;
    align-items: center;
    background-color: var(--color-background);
}

.zoom > p {
    display: inline;
    width: calc(5ch + 2 * var(--tool-area-padding));
    line-height: 1;
    font-size: var(--tool-area-height);
    font-weight: 500;
    border: 1px solid var(--color-border);
    padding: var(--tool-area-padding);
    border-left: none;
    border-right: none;
}

.zoom-display {
    /* Make sure the zoom display doesn't change size. */
    display: inline-block;
    width: 3ch;
    text-align: right;
}
</style>