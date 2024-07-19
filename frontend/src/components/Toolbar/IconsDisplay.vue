<script setup>
import { useToolbarStore } from '@/stores/toolbar';
import { Tool } from '@/util';

import ToolIconButton from '@/components/Toolbar/ToolIconButton.vue';
import IconArea from '@/components/icons/IconArea.vue';
import IconRestrictedArea from '@/components/icons/IconRestrictedArea.vue';
import IconMove from '@/components/icons/IconMove.vue';
import IconQuestion from '@/components/icons/IconQuestion.vue';


const toolbar = useToolbarStore();
</script>

<template>
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
        <div>
            <ToolIconButton
                @click="help_expanded = !help_expanded"
                help_text="Expand the tool help" >
                <IconQuestion />
            </ToolIconButton>
        </div>
    </div>
</template>

<style scoped>
.icons {
    display: flex;
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