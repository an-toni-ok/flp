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
</template>

<style scoped>
.option-list {
    all: unset;
    display: block;
    max-height: calc(var(--input-height) * 7);
    overflow: scroll;
    /* Space for scrollbar */
    width: calc(var(--input-width) + 8px); 
}

.option-container {
    display: flex;
    width: var(--input-width);
    margin-top: -1px;
}

.option-text {
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