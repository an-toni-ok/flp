<script setup>
import { DataOverview } from '@/components';
import { AreaPlanUnchangable } from '@/components/library/drawing';
import { RunList } from '@/components/library/lists';
import { IconOpen } from '@/components/icons';
import { useAreasStore } from '@/stores/areas';
import { useProcessesStore } from '@/stores/processes';
import { useMachinesStore } from '@/stores/machines';
import { computed, onMounted, ref } from 'vue';
import { get_request } from '@/util';

const areasStore = useAreasStore();
const processesStore = useProcessesStore();
const machinesStore = useMachinesStore();

const data = ref([]);
const run_nr = ref(1);
const run_status = ref();
const run_index = ref(0);

const set_current_run_data = (index) => {
    let item = data.value.at(index);
    let item_input = data.value.at(index).input;

    areasStore.reset();
    areasStore.from(item_input.areas, item_input.restricted_areas);
    processesStore.reset();
    processesStore.from(item_input.production_steps);
    machinesStore.machines = item_input.machines;

    run_nr.value = item.nr;
    run_status.value = item.status;
    run_index.value = index
}

const setup = async () => {
    const saved_data_req = await get_request('runs');
    const req_json = await saved_data_req.json();
    data.value = req_json;
    set_current_run_data(run_index.value);
}

const heading = computed(() => {
    return `Durchlauf ${ run_nr.value }`
})

onMounted(() => {
    setup()
})
</script>

<template>
    <div class="side-info">
        <div class="runs">
            <h1>Verlauf</h1>
            <RunList 
                :run_list="data"
                :index="run_index"
                @click="set_current_run_data" />
        </div>
    </div>
    <div class="data-view">
        <div class="headline">
            <h2>{{ heading }}</h2>
            <RouterLink class="link" :to="'run/' + run_nr">
                <span>Öffnen</span>
                <IconOpen />
            </RouterLink>
        </div>
        <DataOverview :bottom_border_only="true" :heading="false" />
        <AreaPlanUnchangable :auto-resize="true" :key="index" />
    </div>
</template>

<style scoped>
.side-info {
    padding: 2rem;
    border-right: 1px solid var(--color-border);
}

.runs > h1 {
    padding-top: 0.25rem;
    margin-bottom: 2rem;
    font-size: var(--font-size-h1);
    line-height: var(--font-size-h1);
}

.data-view {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.headline {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-inline: 1.5rem;
    padding-block: 2rem 0.5rem;
}

.headline > h2 {
    font-size: 1.25rem;
    line-height: 1.25rem;
}

.link {
    display: flex;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    align-items: center;
    border: 1px solid var(--color-border);
    text-decoration: none;
    color: var(--color-text-primary);
}

.link:hover,
.link:focus {
    border-color: var(--color-text-primary);
}

.link > :deep(svg) {
    height: 0.75rem;
    width: 0.75rem;
}

.link > span {
    text-decoration: none;
    height: 1rem;
    line-height: 1rem;
}
</style>