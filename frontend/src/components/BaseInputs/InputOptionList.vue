<script setup>
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
    },
    filteredOptions: {
        type: Array,
        required: true
    }
})

defineEmits(['selected', 'delete'])
</script>

<template>
    <div class="scrollable-content">
        <ul :id="baseId + 'options'"
            class="option-list" >
            <li 
                v-for="option in filteredOptions"
                class="option-container" >
                <div 
                    class="option-text"
                    @click="$emit('selected', option)" >
                    <p>{{ option }}</p>
                </div> 
                <IconButton 
                    v-if="deleteable"
                    @click="$emit('delete', option)"
                    :help_text="'Remove the option ' + option" >
                    <IconRemove />
                </IconButton>           
            </li>
        </ul>
    </div>
</template>

<style scoped>
.scrollable-content {
    --scrollbar-width: 6px;
    display: block;
    width: calc(var(--input-width) + var(--scrollbar-width) * 1.5); 
    max-height: calc(var(--input-height) * 7 - 6px);
    overflow-y: auto;
}

.scrollable-content::-webkit-scrollbar {
    width: var(--scrollbar-width);
}

.scrollable-content::-webkit-scrollbar-thumb {
    width: var(--scrollbar-width);
    border-radius: 50px;
    background-color: var(--color-border);
}

.option-list {
    all: unset;
    width: var(--input-width);
}

.option-container {
    display: flex;
    width: var(--input-width);
    margin-top: -1px;
}

.option-list > .option-container:first-child {
    margin-top: 0;
}

.option-text {
    width: 100%;
    height: var(--input-height);
    display: flex;
    align-items: center;
    justify-content: flex-end;
    font-size: var(--font-size);
    line-height: 1;
    border: 1px solid var(--color-border);
    background-color: var(--color-background);
    text-align: right;
    overflow: hidden;
}

.option-text > p {
    overflow-x: auto;
    overflow-y: hidden;
    height: var(--input-height);
    padding: calc((var(--input-height) - var(--font-size)) / 2);
}

.option-text > p::-webkit-scrollbar {
    height: var(--scrollbar-width);
}

.option-text > p::-webkit-scrollbar-thumb {
    height: var(--scrollbar-width);
    border-radius: 50px;
    background-color: var(--color-border);
}
</style>