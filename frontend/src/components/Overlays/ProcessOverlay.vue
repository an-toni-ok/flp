<script setup>
import { ref } from 'vue';

import NumberInput from '../Inputs/NumberInput.vue';
import TechnologyDropdownInput from '../Inputs/TechnologyDropdownInput.vue';
import OverlayBase from './OverlayBase.vue';

const opened = ref(true)
const technology_value = ref("")
const machine_time = ref(0)
const manual_time = ref(0)
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
        </div>
    </OverlayBase>
</template>

<style scoped>
.overlay-content > * {
    margin: 0 0 0.5rem 0;

}
</style>