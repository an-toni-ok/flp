<script setup>
import { BaseList } from '@/components/library/lists';
import { IconOperator } from '@/components/icons';

const props = defineProps({
    machines: {
        type: Array,
        default: [],
    }
})
</script>

<template>
    <BaseList 
        scroll_start="25rem"
        empty_text="Keine Maschinen wurden erstellt"
        :is_empty="machines.length == 0"
        width="18rem">
        <div v-for="machine in machines" class="machine" >
            <p class="machine-number">{{ machine.id + 1 }}</p>
            <p class="machine-name">{{ machine.name }}</p>
            <div class="operator-nr">
                <IconOperator />
                <p>#{{ machine.operator }}</p>
            </div>
        </div>
    </BaseList>
</template>

<style scoped>
.machine {
    display: flex;
    border: 1px solid var(--color-border);
    border-bottom: none;
    height: calc(2.5rem + 1px);
}

.machine:first-child {
    border-top: none;
}

.machine-number {
    line-height: 2.5rem;
    width: 2.5rem;
    text-align: center;
    font-size: 1.125rem;
    font-weight: 600;
}

.machine-name {
    height: 2.5rem;
    line-height: 2.5rem;
    width: 100%;
}

.operator-nr {
    display: flex;
    height: 2.5rem;
    line-height: 2.5rem;
    align-items: center;
    gap: 5px;
    margin-right: 10px;
}

.operator-nr > :deep(svg) {
    height: 1rem;
    width: 1rem;
}
</style>