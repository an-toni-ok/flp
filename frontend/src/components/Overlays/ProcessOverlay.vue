<script setup>
import { ref } from 'vue';

import NumberInput from '../Inputs/NumberInput.vue';
import TechnologyDropdownInput from '../Inputs/TechnologyDropdownInput.vue';
import OverlayBase from './OverlayBase.vue';
import OverlayButton from '../Buttons/OverlayButton.vue';

const props = defineProps({
    isCreate: {
        type: Boolean,
        default: true
    }
})

const opened = ref(true)
const technology_value = ref("")
const machine_time = ref(0)
const manual_time = ref(0)

const button_text = props.isCreate ? "Erstellen" : "Bearbeiten";
</script>

<template>
    <OverlayBase title="Prozess erstellen">
        <div class="overlay-content" v-show="opened">
            <NumberInput 
                name="Maschinenzeit"
                id="machinenzeit"
                v-model:value="machine_time" />
            <NumberInput 
                name="Manuelle Zeit"
                id="manual-time"
                v-model:value="manual_time" />
            <TechnologyDropdownInput 
                v-model:value="technology_value"
                :is-changeable="true"
                :is-deletable="true" />
            <OverlayButton 
                @click=""
                :text="button_text"/>
        </div>
    </OverlayBase>
</template>

<style scoped>
.overlay-content > * {
    margin: 0 0 0.5rem 0;

}

.overlay-content > button {
    margin-top: 2rem;
}
</style>