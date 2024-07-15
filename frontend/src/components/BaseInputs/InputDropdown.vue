<script setup>
import InputLabel from '../BaseInputs/InputLabel.vue';
import InputError from '../BaseInputs/InputError.vue';

const props = defineProps({
    id: {
        type: String,
        required: true
    },
    name : {
        type: String,
        required: true
    },
    areOptionsShown: {
        type: Boolean,
        required: true
    },
    error: String,
})
</script>

<template>
    <div>
        <InputLabel 
            :id=id
            :name=name />
        <div class="scrollable-content">
            <slot name="header"></slot>
            <div v-show="areOptionsShown" ><!-- div is needed for the v-show here -->
                <slot name="options"></slot>
            </div>
        </div>
        <InputError :error="error" />
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
</style>
