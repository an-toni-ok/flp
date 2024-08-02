<script setup>

import IconButtonDataOverview from '@/components/Buttons/IconButtonDataOverview.vue';
import IconArrowRight from '@/components/icons/IconArrowRight.vue';
import IconArrowLeft from '@/components/icons/IconArrowLeft.vue';

const props = defineProps({
    total: {
        type: Number,
        required: true,
    }
})

// Slide information
const number = defineModel('number');

const incr_number = () => {
    number.value = number.value == props.total ? 1 : number.value + 1
}

const decr_number = () => {
    number.value = number.value == 1 ? props.total : number.value - 1
}
</script>

<template>
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
</template>

<style scoped>
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