<script setup>
import { RunStatus } from '@/util';
import { BaseList } from '@/components/library/lists';

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
</script>

<template>
    <BaseList 
        scroll_start="calc(100vh - 11rem)"
        empty_text="Keine Durchläufe wurden erstellt"
        :is_empty="run_list.length == 0"
        width="22rem">
        <button 
            v-for="(run, index) in run_list"
            class="run"
            @click="$emit('click', index)" >
            <p class="run-name">Durchlauf {{ run.nr }}</p>
            <p class="run-status">{{ new RunStatus(run.status) }}</p>
        </button>
    </BaseList>

    <!-- <div class="run-list">
        <button 
            v-for="(run, index) in run_list"
            class="run"
            @click="$emit('click', index)" >
            <p class="run-name">Durchlauf {{ run.nr }}</p>
            <div class="run-status">
                <p>{{ new RunStatus(run.status) }}</p>
            </div>
        </button>
    </div> -->
</template>

<style scoped>
.run {
    position: relative;
    display: flex;
    border: 1px solid var(--color-border);
    border-bottom: none;
    height: calc(2.5rem + 1px);
    padding-inline: 15px;
    justify-content: space-between;
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
    text-align: left;
    text-wrap: nowrap;
}

.run-status {
    height: 2.5rem;
    line-height: 2.5rem;

}
</style>