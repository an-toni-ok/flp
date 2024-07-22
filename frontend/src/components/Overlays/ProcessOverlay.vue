<script setup>
import { ref } from 'vue';

import { useProcessesStore } from '@/stores/processes';
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

const processesStore = useProcessesStore();

const button_text = props.isCreate ? "Erstellen" : "Bearbeiten";
</script>

<template>
    <OverlayBase title="Prozess erstellen">
        <div class="overlay-content" v-show="opened">
            <NumberInput 
                name="Maschinenzeit"
                id="machinenzeit"
                v-model:value="processesStore.input_machine_time" />
            <NumberInput 
                name="Manuelle Zeit"
                id="manual-time"
                v-model:value="processesStore.input_manual_time" />
            <TechnologyDropdownInput 
                v-model:value="processesStore.input_technology"
                :is-changeable="true"
                :is-deletable="true" />
            <OverlayButton 
                @click="processesStore.set"
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