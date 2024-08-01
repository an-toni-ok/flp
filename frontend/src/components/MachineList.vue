<script setup>
import { useMachinesStore } from '@/stores/machines';

const machinesStore = useMachinesStore();
</script>

<template>
    <div class="machines-list">
        <div 
            v-for="(machine, index) in machinesStore.machines"
            class="machine" >
            <p class="machine-number">{{ index + 1 }}</p>
            <p class="machine-name">{{ machine.machine_type }}</p>
        </div>
    </div>
</template>

<style scoped>
.machine {
    display: flex;
    border: 1px solid var(--color-border);
    border-bottom: none;
    height: 2.5rem;
}

.machine:last-child {
    border-bottom: 1px solid var(--color-border);
}

.machine-number {
    line-height: 2.5rem;
    width: 2.5rem;
    text-align: center;
    font-size: 1.125rem;
    font-weight: 600;
}

.machine-name {
    line-height: 2.5rem;
}

.inputs {
    display: flex;
    /* flex-direction: column; */
    /* justify-content: space-between; */
    gap: 4rem;
    padding: 1.5rem;
    border: 1px solid var(--color-border);
}

.checkboxes {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: flex-end;
}

.general-inputs {
    margin-bottom: 4px;
}

.general-inputs > h2 {
    font-size: var(--font-size-h3);
    margin-bottom: 1.5rem;
}

.general-inputs > *:not(h2),
.checkboxes > *:not(h2) {
    margin-top: 0.5rem;
}
</style>