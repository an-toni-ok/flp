<script setup>
import { ref } from 'vue';
import { useToolbarStore } from '@/stores/toolbar';
import { Tool } from '@/util';
import ToolIconButton from './Buttons/ToolIconButton.vue';
import IconArea from './icons/IconArea.vue';
import IconRestrictedArea from './icons/IconRestrictedArea.vue';
import IconMove from './icons/IconMove.vue';
import IconQuestion from './icons/IconQuestion.vue';
import IconZoomMinus from './icons/IconZoomMinus.vue';
import IconZoomPlus from './icons/IconZoomPlus.vue';

const toolbar = useToolbarStore();
const help_expanded = ref(false);
</script>

<template>
    <div class="tool-area">
        <div class="tool-area-name">
            <h3>Werkzeuge</h3>
            <div 
                class="tool-area-info"
                :class="{ 'opened': help_expanded }">
                <ToolIconButton
                    @click="help_expanded = !help_expanded"
                    help_text="Expand the tool help" >
                    <IconQuestion />
                </ToolIconButton>
                <p v-show="help_expanded" class="tool-help-text">
                    This is a tool tip for the tools
                </p>
            </div>
        </div>
        <div class="icons">
            <div class="area" 
                :class="{ 'selected': toolbar.isActive(Tool.Area) }" >
                <ToolIconButton 
                    @click="toolbar.setTool(Tool.Area)"
                    help_text="Tool to draw an area." >
                    <IconArea />
                </ToolIconButton>
            </div>
            <div class="r-area"
                :class="{ 'selected': toolbar.isActive(Tool.RestrictedArea) }" >
                <ToolIconButton 
                    @click="toolbar.setTool(Tool.RestrictedArea)"
                    help_text="Tool to draw a restricted area." >
                    <IconRestrictedArea />
                </ToolIconButton>
            </div>
            <div class="move"
                :class="{ 'selected': toolbar.isActive(Tool.Move) }" >
                <ToolIconButton 
                    @click="toolbar.setTool(Tool.Move)"
                    help_text="Tool to move the plan around." >
                    <IconMove />
                </ToolIconButton>
            </div>
        </div>
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
    </div>
</template>

<style scoped>
.tool-area {
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 2rem;
}

.tool-area-name {
    display: flex;
    align-items: center;
}

.tool-area-name > h3,
.zoom > p {
    line-height: 1;
    font-size: var(--tool-area-height);
    font-weight: 500;
    border: 1px solid var(--color-border);
    padding: var(--tool-area-padding);
}

.tool-area-name > h3 {
    border-right: none;
}

.tool-area-info {
    position: relative;
}

.tool-help-text {
    border: 1px solid var(--color-border);
    padding: 0.5rem;
    --icon-measurement: calc(var(--tool-area-height) + 2* var(--tool-area-padding) + 2px);
    --half-width: 6rem;
    position: absolute; 
    left: calc(-1* var(--half-width) + var(--icon-measurement) / 2);
    top: calc(var(--icon-measurement) / 2 + 10px + 1.25rem);
    width: calc(2 * var(--half-width));
    z-index: 1;
    line-height: 1.2;
}

.icons {
    display: flex;
}

.opened > button,
.tool-help-text,
.selected > button {
    background-color: rgba(var(--color-brand-rgb), 0.1);
}

.area > button > svg {
    stroke: var(--color-area);
}

.r-area > button > svg {
    stroke: var(--color-restricted-area);
}

.zoom {
    display: flex;
    align-items: center;
}

.zoom > p {
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
