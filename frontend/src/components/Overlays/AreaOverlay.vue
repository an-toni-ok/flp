<script setup>
import { ref } from 'vue';

import NumberInput from '../Inputs/NumberInput.vue';
import OverlayBase from './OverlayBase.vue';

const opened = ref(true)

const height = ref(0)
const width = ref(0)
const x_pos = ref(0)
const y_pos = ref(0)
</script>

<template>
    <OverlayBase title="Fläche erstellen">
        <div class="overlay-content" v-show="opened">
            <div class="input-split">
                <h2>Fläche</h2>
                <NumberInput 
                    name="Breite"
                    id="breite"
                    v-model:value="width" />
                <NumberInput 
                    name="Höhe"
                    id="hoehe"
                    v-model:value="height" />
            </div>

            <div class="input-split">
                <h2>Position</h2>
                <NumberInput 
                    name="x-Position"
                    id="x-pos"
                    v-model:value="x_pos" />
                <NumberInput 
                    name="y-Position"
                    id="y-pos"
                    v-model:value="y_pos" />
            </div>
        </div>
    </OverlayBase>
</template>

<style scoped>
.overlay-content {
    margin: 2em 0;
}

.input-split > * {
    margin: 0.5rem 0 0 0;
}

.input-split > h2 {
    margin: 2rem 0 0 0;
    font-size: var(--font-size-h3);
}
</style>