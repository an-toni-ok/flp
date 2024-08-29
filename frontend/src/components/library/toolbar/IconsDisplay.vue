<script setup>
import { useToolbarStore } from '@/stores/toolbar';
import { Tool } from '@/util';
import { IconButton } from '@/components/library/buttons';
import { IconArea, IconRestrictedArea, IconMove, IconQuestion, IconDelete } from '@/components/icons';


const toolbar = useToolbarStore();
</script>

<template>
    <div class="icons">
        <div class="area" 
            :class="{ 'selected': toolbar.isActive(Tool.Area) }" >
            <IconButton 
                @click="toolbar.setTool(Tool.Area)"
                text="Freifläche zeichnen" >
                <IconArea />
            </IconButton>
        </div>
        <div class="r-area"
            :class="{ 'selected': toolbar.isActive(Tool.RestrictedArea) }" >
            <IconButton 
                @click="toolbar.setTool(Tool.RestrictedArea)"
                text="Sperrfläche zeichnen" >
                <IconRestrictedArea />
            </IconButton>
        </div>
        <div class="move"
            :class="{ 'selected': toolbar.isActive(Tool.Move) }" >
            <IconButton 
                @click="toolbar.setTool(Tool.Move)"
                text="Flächen bewegen und verändern" >
                <IconMove />
            </IconButton>
        </div>
        <div :class="{ 'selected': toolbar.isActive(Tool.Delete)}" >
            <IconButton
                @click="toolbar.setTool(Tool.Delete)"
                text="Flächen löschen" >
                <IconDelete />
            </IconButton>
        </div>
        <div>
            <IconButton
                @click="help_expanded = !help_expanded"
                text="Die Einführung öffnen" >
                <IconQuestion />
            </IconButton>
        </div>
    </div>
</template>

<style scoped>
.icons {
    display: flex;
    background-color: var(--color-background);
}

.icons > :deep(:not(:first-child)) {
    margin-left: -1px;
}

.selected > button {
    background-color: rgba(var(--color-brand-rgb), 0.1);
}

.area > :deep(button > div > svg) {
    stroke: var(--color-area);
}

.r-area :deep(button > div > svg) {
    stroke: var(--color-restricted-area);
}
</style>