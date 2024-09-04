<script setup>
import { DataOverview } from '@/components';
import { AreaPlanUnchangable } from '@/components/library/drawing';
import { RunList } from '@/components/library/lists';
import { useAreasStore } from '@/stores/areas';
import { useProcessesStore } from '@/stores/processes';
import { useMachinesStore } from '@/stores/machines';
import { onMounted, ref } from 'vue';
import { get_request } from '@/util';

const areasStore = useAreasStore();
const processesStore = useProcessesStore();
const machinesStore = useMachinesStore();

const data = ref([]);
const run_nr = ref();
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

onMounted(() => {
    setup()
})
</script>

<template>
    <div class="side-info">
        <div class="runs">
            <h1>Durchläufe</h1>
            <RunList 
                :run_list="data"
                :index="run_index"
                @click="set_current_run_data" />
        </div>
    </div>
    <div class="data-view">
        <DataOverview />
        <AreaPlanUnchangable :auto-resize="true" :key="index" />
    </div>
</template>

<style>
.side-info {
    padding: 2rem;
    border-right: 1px solid var(--color-border);
}

.runs > h1 {
    margin-bottom: 2rem;
    font-size: var(--font-size-h1);
}

.data-view {
    display: flex;
    flex-direction: column;
    width: 100%;
}
</style>