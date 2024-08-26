<script setup>
import { InputLabel, InputError } from '.'

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
        <div class="option-list" v-show="areOptionsShown" ><!-- div is needed for the v-show here -->
            <slot name="options"></slot>
        </div>
        <InputError :error="error" />
    </div>
</template>

<style scoped>
.option-list {
    margin-top: -2px;
}
</style>
