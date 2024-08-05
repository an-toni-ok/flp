<script setup>
import IconCycleTime from '../icons/IconCycleTime.vue';
import IconInvestment from '../icons/IconInvestment.vue';
import IconOperator from '../icons/IconOperator.vue';
import IconPart from '../icons/IconPart.vue';
import IconSpace from '../icons/IconSpace.vue';

const props = defineProps({
    stats: {
        type: Object,
        default: undefined
    }
})
</script>

<template>
    <div class="stats-list" v-if="stats != undefined">
        <div class="stat-display" data-info="Zykluszeit">
            <IconCycleTime />
            <p>{{ props.stats.cycle_time }}</p>
        </div>
        <div class="stat-display" data-info="Stückkosten">
            <IconPart />
            <p>{{ props.stats.objectives.cost_per_part }}&#8364;</p>
        </div>
        <div class="stat-display" data-info="Investition">
            <IconInvestment />
            <p>{{ props.stats.objectives.invest }}&#8364;</p>
        </div>
        <div class="stat-display" data-info="Benutzte Fläche">
            <IconSpace />
            <p>{{ props.stats.objectives.used_area }}</p>
        </div>
        <div class="stat-display" data-info="Arbeiteranzahl">
            <IconOperator />
            <p>{{ props.stats.objectives.number_operators }}</p>
        </div>
    </div>
</template>

<style scoped>
.stats-list {
    border: 1px solid var(--color-border);
    border-top: 0;
    display: flex;
    flex-wrap: wrap;
    padding: 1rem;
    gap: 1rem;
    margin-left: -1px;
}

.stat-display {
    width: calc(50% - 0.5rem);
    position: relative;
    display: flex;
    height: 1.5rem;
    line-height: 1.5rem;
    align-items: center;
    gap: 0.5rem;
}

.stat-display::after {
    content: attr(data-info);
    z-index: 1;
    right: 0;
    top: 75%;
    position: absolute;
    background-color: var(--color-background);
    padding: 0.5rem;
    border: 1px solid var(--color-border);
    height: 1rem;
    line-height: 1rem;
    transform: scale(0);
}

.stat-display:hover::after {
    transform: scale(1);
}

.stat-display > svg {
    height: 1rem;
    width: 1rem;
}

</style>