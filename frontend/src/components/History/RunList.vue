<script setup>
import { RunStatus } from '@/util';

const props = defineProps({
    run_list: {
        type: Array,
        default: [],
    },
    setIndex: {
        type: Number,
    }
})

defineEmits(['click'])
console.log(props.run_list);
</script>

<template>
    <div class="run-list">
        <button 
            v-for="(run, index) in run_list"
            class="run"
            @click="$emit('click', index)" >
            <p class="run-name">Durchlauf {{ run.nr }}</p>
            <div class="run-status">
                <p>{{ new RunStatus(run.status) }}</p>
            </div>
        </button>
    </div>
</template>

<style scoped>
.run-list {
    --scrollbar-width: 6px;
    max-height: calc(100vh - 12rem);
    overflow-y: auto;
    border: 1px solid var(--color-border);
    border-left: none;
    border-right: none;
    margin-bottom: 2rem;
}

.run-list::-webkit-scrollbar {
    width: var(--scrollbar-width);
    border-right: 1px solid var(--color-border);
}

.run-list::-webkit-scrollbar-thumb {
    width: var(--scrollbar-width);
    border-radius: 50px;
    background-color: var(--color-border);
}

.run {
    position: relative;
    display: flex;
    border: 1px solid var(--color-border);
    border-bottom: none;
    height: calc(2.5rem + 1px);
    gap: 5rem;
}

.run:hover {
    cursor: pointer;
}

.run:first-child {
    border-top: none;
}

.run-name {
    height: 2.5rem;
    line-height: 2.5rem;
    margin-left: 10px;
    text-align: left;
    text-wrap: nowrap;
}

.run-status {
    height: 2.5rem;
    line-height: 2.5rem;
    margin-right: 10px;
}
</style>