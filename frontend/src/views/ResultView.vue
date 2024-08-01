<script setup>
import { ref } from 'vue';

import AreaPlan from '@/components/DrawingArea/AreaPlan.vue';
import IconButtonDataOverview from '@/components/Buttons/IconButtonDataOverview.vue';
import IconArrowRight from '@/components/icons/IconArrowRight.vue';
import IconArrowLeft from '@/components/icons/IconArrowLeft.vue';
import MachineList from '@/components/MachineList.vue';

// Slide information
const title = "Optimierungsergebnisse";
const number = ref(1);
const total = ref(3);

const incr_number = () => {
    number.value = number.value == total.value ? 1 : number.value + 1
}

const decr_number = () => {
    number.value = number.value == 1 ? total.value : number.value - 1
}
</script>

<template>
    <div class="expand">
        <div class="view-content">
            <div class="view-data">
                <div class="view-data-header">
                    <h1>{{ title }}</h1>
                </div>
                <!-- Main content -->
                <div class="result-selection">
                    <IconButtonDataOverview
                        help_text="Zurück"
                        @click="decr_number">
                        <IconArrowLeft />
                    </IconButtonDataOverview>
                    <div class="result-selection-heading-container">
                        <div class="result-selection-heading">
                            <h1>Ergebnis</h1>
                            <p>{{ number }} von {{ total }}</p>
                        </div>
                    </div>
                    <IconButtonDataOverview
                        help_text="Weiter"
                        @click="incr_number">
                        <IconArrowRight />
                    </IconButtonDataOverview>
                </div>
                <MachineList />
            </div>
        </div>
        <div class="side-content">
            <AreaPlan />
        </div>
    </div>
</template>

<style scoped>
.expand {
	width: 100%;
    height: 100%;
    display: inline-flex;
    overflow: hidden;
}

.view-content {
    width: fit-content;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-block: var(--site-margin-tb);
    padding-inline: var(--site-margin-lr);
    border-right: 1px solid var(--color-border);
    background-color: var(--color-background);
}

.view-data {
    display: flex;
    flex-direction: column;
    gap:  calc(var(--input-height) + var(--tool-area-padding));;
}

.view-data-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    background-color: var(--color-background);
    border: 1px solid var(--color-border);
    gap: 2rem;
    padding: var(--tool-area-padding) 1.5rem;
}

.view-data-header > h1 {
    line-height: 1;
    font-size: var(--tool-area-height);
    font-weight: 500;
}

.view-data-header > p {
    line-height: 1;
    font-size: 0.8rem;
}

.result-selection {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.result-selection-heading-container {
    height: 100%;
    width: 100%;
    border-top: 1px solid var(--color-border);
    border-bottom: 1px solid var(--color-border);
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 18rem;
}

.result-selection-heading {
    display: flex;
    align-items: flex-end;
    gap: 1rem;
}

.result-selection-heading > h1 {
    line-height: 1;
    font-size: var(--tool-area-height);
    font-weight: 500;
}

.result-selection-heading > p {
    line-height: 1;
    font-size: 0.8rem;
}

.side-content {
    width: 100%;
    height: 100%;
}
</style>