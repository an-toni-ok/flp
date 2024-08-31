<script setup>
import { IconButton } from '@/components/library/buttons';
import { IconArrowRight, IconArrowLeft, IconCycleTime, IconPart, IconInvestment, IconSpace, IconOperator } from '@/components/icons';

import { StatDisplay } from '@/components/library/util';

const props = defineProps({
    number: {
        type: Number,
        required: true,
    },
    total: {
        type: Number,
        required: true,
    },
    stats: {
        type: Object,
        default: undefined
    }
})

const emits = defineEmits(['incr', 'decr'])
</script>

<template>
    <!-- Heading -->
    <div class="result-selection">
        <IconButton
            text="Zurück"
            @click="$emit('decr')">
            <IconArrowLeft />
        </IconButton>
        <div class="result-selection-heading">
            <h1>Ergebnis</h1>
            <p>{{ number }} von {{ total }}</p>
        </div>
        <IconButton
            text="Weiter"
            @click="$emit('incr')">
            <IconArrowRight />
        </IconButton>
    </div>

    <!-- Stats -->
    <div class="stats-list" v-if="stats != undefined">
        <StatDisplay :text="props.stats.cycle_time" 
            info_name="Zykluszeit">
            <IconCycleTime />
        </StatDisplay>

        <StatDisplay :text="props.stats.objectives.cost_per_part" 
            info_name="Stückkosten">
            <IconPart />
        </StatDisplay>

        <StatDisplay :text="props.stats.objectives.invest" 
            info_name="Investition">
            <IconInvestment />
        </StatDisplay>

        <StatDisplay :text="props.stats.objectives.used_area" 
            info_name="Benutzte Fläche">
            <IconSpace />
        </StatDisplay>
        
        <StatDisplay :text="props.stats.objectives.number_operators" 
            info_name="Arbeiteranzahl">
            <IconOperator />
        </StatDisplay>
    </div>
</template>

<style>
.result-selection {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.result-selection-heading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    height: 2.5rem;
    border-top: 1px solid var(--color-border);
    border-bottom: 1px solid var(--color-border);
    min-width: 18rem;
}

.result-selection-heading > h1 {
    line-height: 1rem;
    font-size: 1rem;
    font-weight: 500;
}

.result-selection-heading > p {
    line-height: 1;
    font-size: 0.8rem;
    padding-top: 0.2rem;
}

.stats-list {
    border: 1px solid var(--color-border);
    border-top: 0;
    display: flex;
    flex-wrap: wrap;
    padding: 1rem;
    gap: 1rem;
}
</style>