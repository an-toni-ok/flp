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
    display: block;
    max-height: calc(var(--input-height) * 7);
    overflow-x: scroll;
    /* Space for scrollbar */
    width: calc(var(--input-width) + 8px); 
}
</style>
