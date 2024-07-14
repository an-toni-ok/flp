<script setup>
import { useTechnologiesStore } from '@/stores/technologies';

import IconButton from '../BaseInputs/IconButton.vue';
import IconRemove from '../icons/IconRemove.vue';

const props = defineProps({
    baseId: {
        type: String,
        required: true,
    },
    deleteable: {
        type: Boolean,
        default: true,
    }
})

defineEmits(['selected'])

const technologiesStore = useTechnologiesStore();
</script>

<template>
    <ul :id="baseId + 'options'"
        class="tech-option-list" 
        role="listbox" 
        aria-label="List of already set technologies" >
        <li 
            v-for="tech in technologiesStore.technologies"
            class="tech-option"
            @click="$emit('selected', tech)"
            role="option" >
            <div class="list-option" >
                <p>{{ tech }}</p>
            </div> 
            <IconButton 
                v-if="deleteable"
                @click="technologiesStore.remove(tech)"
                :help_text="'Remove the technology ' + tech"
                :without-top-border="false" >
                <IconRemove />
            </IconButton>           
        </li>
    </ul>
</template>

<style scoped>
.tech-option-list {
    all: unset;
    display: block;
    max-height: calc(var(--input-height) * 7);
    overflow: scroll;
    /* Space for scrollbar */
    width: calc(var(--input-width) + 8px); 
}

.tech-option {
    display: flex;
    width: var(--input-width);
    margin-top: -1px;
}

.list-option {
    width: 100%;
    height: var(--input-height);
    display: flex;
    align-items: center;
    justify-content: flex-end;
    font-size: var(--font-size);
    line-height: 1;
    padding-right: calc((var(--input-height) - var(--font-size)) / 2);
    border: 1px solid var(--color-border);
    background-color: var(--color-background);
    text-align: right;
}
</style>