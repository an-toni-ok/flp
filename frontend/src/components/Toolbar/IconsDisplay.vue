<script setup>
import { useToolbarStore } from '@/stores/toolbar';
import { Tool } from '@/util';

import ToolIconButton from '@/components/Toolbar/ToolIconButton.vue';
import IconArea from '@/components/icons/IconArea.vue';
import IconRestrictedArea from '@/components/icons/IconRestrictedArea.vue';
import IconMove from '@/components/icons/IconMove.vue';
import IconQuestion from '@/components/icons/IconQuestion.vue';
import IconDelete from '../icons/IconDelete.vue';


const toolbar = useToolbarStore();
</script>

<template>
    <div class="icons">
        <div class="area" 
            :class="{ 'selected': toolbar.isActive(Tool.Area) }" >
            <ToolIconButton 
                @click="toolbar.setTool(Tool.Area)"
                help_text="Freifläche zeichnen" >
                <IconArea />
            </ToolIconButton>
        </div>
        <div class="r-area"
            :class="{ 'selected': toolbar.isActive(Tool.RestrictedArea) }" >
            <ToolIconButton 
                @click="toolbar.setTool(Tool.RestrictedArea)"
                help_text="Sperrfläche zeichnen" >
                <IconRestrictedArea />
            </ToolIconButton>
        </div>
        <div class="move"
            :class="{ 'selected': toolbar.isActive(Tool.Move) }" >
            <ToolIconButton 
                @click="toolbar.setTool(Tool.Move)"
                help_text="Flächen bewegen und verändern" >
                <IconMove />
            </ToolIconButton>
        </div>
        <div :class="{ 'selected': toolbar.isActive(Tool.Delete)}" >
            <ToolIconButton
                @click="toolbar.setTool(Tool.Delete)"
                help_text="Flächen löschen" >
                <IconDelete />
            </ToolIconButton>
        </div>
        <div>
            <ToolIconButton
                @click="help_expanded = !help_expanded"
                help_text="Die Einführung öffnen" >
                <IconQuestion />
            </ToolIconButton>
        </div>
    </div>
</template>

<style scoped>
.icons {
    display: flex;
    background-color: var(--color-background);
}

.selected > button {
    background-color: rgba(var(--color-brand-rgb), 0.1);
}

.area > button > svg {
    stroke: var(--color-area);
}

.r-area > button > svg {
    stroke: var(--color-restricted-area);
}
</style>