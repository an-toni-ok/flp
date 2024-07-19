<script setup>
import { ref } from 'vue';
import ToolIconButton from './Buttons/ToolIconButton.vue';
import IconQuestion from './icons/IconQuestion.vue';
import ZoomDisplay from './Toolbar/ZoomDisplay.vue';
import IconsDisplay from './Toolbar/IconsDisplay.vue';

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
}

.tool-area-name > h3 {
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
</style>
