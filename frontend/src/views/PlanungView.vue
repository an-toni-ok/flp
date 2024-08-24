<script setup>
import { onMounted } from 'vue';

import { PlanningState, get_request } from '@/util';
import { usePlanningStore } from '@/stores/planning';
import { useAreasStore } from '@/stores/areas';
import { useProcessesStore } from '@/stores/processes';
import { useMachinesStore } from '@/stores/machines';
import { useSettingsStore } from '@/stores/settings';

import AreaView from './AreaView.vue';
import ProcessView from './ProcessView.vue';
import MachineView from './MachineView.vue';
import ConfigurationView from './ConfigurationView.vue';
import WaitingView from './WaitingView.vue';
import ResultView from './ResultView.vue';

// The id prop gets passed by the router 
// (and is only supplied if a specific run is 
// opened from the history view.)
const props = defineProps({
    id: {
        type: Number,
        default: undefined,
    }
})

const planningStore = usePlanningStore();

const areasStore = useAreasStore();
const processesStore = useProcessesStore();
const machinesStore = useMachinesStore();
const settingsStore = useSettingsStore();

const setup = async (load_id) => {
    // Load specified run or current if none is specified.
    let route = undefined;
    if (load_id != undefined) {
        route = `/input/${load_id}`;
    } else {
        route = 'load'
    }

    const saved_data_req = await get_request(route);
    const req_json = await saved_data_req.json();
    const status = req_json.status
    const data = req_json.data

    if (status == "RUNNING") {
        areasStore.from(data.areas, data.restricted_areas);
        planningStore.setState(PlanningState.Waiting);
        return
    }
    if (status == "COMPLETED") {
        areasStore.from(data.areas, data.restricted_areas);
        planningStore.setState(PlanningState.Result);
        return
    }

    if (data.areas.length == 0) {
        planningStore.setState(PlanningState.Areas);
        return
    }
    areasStore.from(data.areas, data.restricted_areas);

    if (data.production_steps.length == 0) {
        planningStore.setState(PlanningState.Processes);
        return
    }
    processesStore.from(data.production_steps);

    if (data.machines.length == 0) {
        planningStore.setState(PlanningState.Machines);
        return
    }
    machinesStore.machines = data.machines;
    
    if (Object.keys(data.objectives).length == 0) {
        planningStore.setState(PlanningState.Configuration)
        return
    }
    settingsStore.from(
        data.objectives, 
        data.target_cycle_time,
        data.hourly_operator_cost
    );
    planningStore.setState(PlanningState.Configuration);
}

onMounted(() => {
    setup(props.id)
})
</script>

<template>
    <AreaView 
        v-if="planningStore.isActive(PlanningState.Areas)" />
    <ProcessView 
        v-if="planningStore.isActive(PlanningState.Processes)" />
    <MachineView 
        v-if="planningStore.isActive(PlanningState.Machines)" />
    <ConfigurationView 
        v-if="planningStore.isActive(PlanningState.Configuration)" />
    <WaitingView 
        v-if="planningStore.isActive(PlanningState.Waiting)" />
    <ResultView 
        v-if="planningStore.isActive(PlanningState.Result)"
        :result_id="id" />
</template>

<style scoped>
</style>