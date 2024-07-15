<script setup>
import { ref, computed } from 'vue';
import { useTechnologiesStore } from '@/stores/technologies';

import InputLabel from '../BaseInputs/InputLabel.vue';
import InputError from '../BaseInputs/InputError.vue';
import InputDropdownHeader from '../BaseInputs/InputDropdownHeader.vue';
import InputDropdownOptionList from '../BaseInputs/InputDropdownOptionList.vue';

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
// const technologiesStore = useTechnologiesStore();
// const filteredTechnologies = computed(() => {
//     if (!value.value) {
//       return technologiesStore.technologies
//     }
//     return technologiesStore.technologies.filter((tech) => tech.includes(value.value))
// })

// const optionClicked = (option) => {
//     value.value = option
// }
// const toggleOptions = () => {
//     areOptionsShown.value = !areOptionsShown.value
// }
// const addHandler = (value) => {
//     if (props.isChangeable) {
//         technologiesStore.add(value)
//     }
// }
// const deleteHandler = (value) => {
//     technologiesStore.remove(value)
// }
</script>

<template>
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
