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
    hasLabel: {
        type: Boolean,
        default: true
    },
    error: String,
})
</script>

<template>
    <div>
        <InputLabel
            v-if="hasLabel"
            :id=id
            :name=name />
        <slot name="header"></slot>
        <div v-show="areOptionsShown" ><!-- div is needed for the v-show here -->
            <slot name="options"></slot>
        </div>
        <InputError :error="error" />
    </div>
</template>

<style scoped>
</style>
