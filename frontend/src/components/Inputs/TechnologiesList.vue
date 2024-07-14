<script setup>
import { useTechnologiesStore } from '@/stores/technologies';

import IconButton from './IconButton.vue';
import IconRemove from '../icons/IconRemove.vue';

const props = defineProps({
    isFocused: {
        type: Boolean,
        required: true,
    },
    deleteable: {
        type: Boolean,
        default: true,
    }
})

defineEmits(['selected', 'focus', 'blur'])

const technologiesStore = useTechnologiesStore();
</script>

<template>
    <ul class="tech-option-list" role="listbox" aria-label="Already set technologies">
        <li 
            v-for="tech in technologiesStore.technologies"
            class="tech-option"
            @click="$emit('selected', tech)"
            role="option" >
            <div 
                class="tech-display"
                :class="{ 'focus': isFocused, 'non-deleteable': !deleteable }">
                <p>{{ tech }}</p>
            </div> 
            <IconButton 
                v-if="deleteable"
                @click="technologiesStore.remove(tech)"
                help_text="Remove the technology."
                :without-top-border="true"
                :is-focused="isFocused" >
                <IconRemove />
            </IconButton>           
        </li>
    </ul>
</template>

<style scoped>
.tech-option-list {
    all: unset;
    width: 210px;
}

.tech-option {
    display: flex;
}

.tech-display {
    box-sizing: border-box;
    height: 30px;
    border: 1px solid var(--color-border);
    border-top: none;
    margin: 0;
    padding: 0;
    background-color: var(--color-background);
    text-align: right;
    padding-right: 10px;
    width: 180px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
}

.non-deleteable {
    width: 210px;
}

.focus {
    border-color: var(--color-text-primary);
    color: var(--color-text-primary);
}
</style>