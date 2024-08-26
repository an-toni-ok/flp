<script setup>
import { IconRemove } from '@/components/icons';
import { IconButton } from '@/components/library/buttons';
import { Scrollbar } from '@/components/library/styling';

const props = defineProps({
    baseId: {
        type: String,
        required: true,
    },
    deleteable: {
        type: Boolean,
        default: true,
    },
    filteredOptions: {
        type: Array,
        required: true
    }
})

defineEmits(['selected', 'delete'])
const scroll_start = "8.5rem";
</script>

<template>
    <div class="option-display">
        <Scrollbar :scroll-start="scroll_start">
            <ul :id="baseId + 'options'" class="option-list">
                <li v-for="option in filteredOptions"
                    class="option-container" >
                    <IconButton 
                        v-if="deleteable"
                        @click="$emit('delete', option)"
                        :small="true"
                        tooltipPosition="right"
                        text="Entfernen" >
                        <IconRemove />
                    </IconButton>      
                    <button 
                        class="option-text"
                        @click="$emit('selected', option)"
                        :data-option="option + ' auswählen'" >
                        <p>{{ option }}</p>
                    </button>      
                </li>
            </ul>
        </Scrollbar>
    </div>
</template>

<style scoped>
.option-display {
    width: var(--input-width);
}

.option-list {
    /* 
    Without these two pixels an overflow is caused regardless
    of the height of the container. do not remove! */
    padding: 1px 0;
}

.option-display > :deep(.scrollbar) {
    border-top: none;
}

.option-container {
    display: flex;
    margin-top: -1px;
}

.option-container:first-child {
    margin-top: 0;
}

.option-text {
    position: relative;
    height: var(--input-height);
    font-size: var(--font-size);
    border: 1px solid var(--color-border);
    background-color: var(--color-background);
    text-align: left;
    margin-left: -1px;
}

.option-text:hover {
    cursor: pointer;
}

.option-text:focus {
    outline: none;
    border-color: var(--color-text-primary);
    z-index: 1;
}

.option-text > p {
    line-height: var(--input-height);
    padding: 0 0.5rem;
}

.option-container:last-child > .option-text,
.option-container:last-child > :deep(.icon-button) {
    border-bottom: none;
}

.option-container:last-child > .option-text:focus,
.option-container:last-child > :deep(.icon-button:focus) {
    border-bottom: 1px solid var(--color-text-primary);
}
</style>