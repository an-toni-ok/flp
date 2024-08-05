<script setup>
import IconOperator from '../icons/IconOperator.vue';

const props = defineProps({
    machines: {
        type: Array,
        default: [],
    }
})
</script>

<template>
    <div class="machines-list">
        <div 
            v-for="(machine, index) in machines"
            class="machine" >
            <p class="machine-number">{{ index + 1 }}</p>
            <p class="machine-name">{{ machine.name }}</p>
            <div class="operator-nr">
                <IconOperator />
                <p>#{{ machine.operator }}</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.machines-list {
    --scrollbar-width: 6px;
    max-height: calc(100vh - 24rem);
    overflow-y: auto;
    border: 1px solid var(--color-border);
    border-left: none;
    border-right: none;
}

.machines-list::-webkit-scrollbar {
    width: var(--scrollbar-width);
    border-right: 1px solid var(--color-border);
}

.machines-list::-webkit-scrollbar-thumb {
    width: var(--scrollbar-width);
    border-radius: 50px;
    background-color: var(--color-border);
}

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

.operator-nr > svg {
    height: 1rem;
    width: 1rem;
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