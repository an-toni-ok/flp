<script setup>
import { useToolbarStore } from '@/stores/toolbar';

import { IconButton } from '@/components/library/buttons';
import { IconZoomPlus, IconZoomMinus } from '@/components/icons';

const toolbar = useToolbarStore();
</script>

<template>
    <div class="zoom">
        <IconButton 
            text="Zoomfaktor verringern"
                @click="toolbar.lowerZoom()" >
            <IconZoomMinus />
        </IconButton>
        <p><span class="zoom-display">{{ toolbar.zoom }}</span> %</p>
        <IconButton 
            text="Zoomfaktor erhöhen"
                @click="toolbar.raiseZoom()" >
            <IconZoomPlus />
        </IconButton>
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
    width: fit-content;
    height: 2.5rem;
    line-height: 2.5rem;
    font-size: var(--tool-area-height);
    font-weight: 500;
    border: 1px solid var(--color-border);
    padding: 0 var(--tool-area-padding);
    border-left: none;
    border-right: none;
    text-wrap: nowrap;
}

.zoom-display {
    /* Make sure the zoom display doesn't change size. */
    display: inline-block;
    min-width: 3ch;
    text-align: right;
}
</style>