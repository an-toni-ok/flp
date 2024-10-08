<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { DrawingShape, PlanningState, get_request } from '@/util';
import { useAreasStore } from '@/stores/areas';
import { usePlanningStore } from '@/stores/planning';
import { useProcessesStore } from '@/stores/processes';
import { useMachinesStore } from '@/stores/machines';
import { useSettingsStore } from '@/stores/settings';

import { MachineList } from '@/components/library/lists';
import { ResultStatDisplay } from '@/components/library/util';
import { IconButton } from '@/components/library/buttons';
import { DrawingArea } from '@/components';
import { ZoomDisplay } from '@/components/library/toolbar';
import { IconPlus } from '@/components/icons';

const props = defineProps({
    result_id: {
        type: Number,
        default: undefined,
    }
})

const areasStore = useAreasStore();
const router = useRouter();

// Slide information
const title = "Optimierungsergebnisse";
const number = ref(1);
const total = ref(3);

const result_machine_list = ref([]);
const result_stats = ref({})
const results = ref()

const get_results = async () => {
    let route = undefined;
    if (props.result_id != undefined) {
        route = `/output/${props.result_id}`;
    } else {
        route = 'optimize'
    }

    const optimize_result = await get_request(route);
    const json_result = await optimize_result.json();
    results.value = json_result.output;
    total.value = results.value.length;
    set_current_result(number.value);
}

const convert_to_grid_size = (measurement) => {
    return measurement * 10 * areasStore.unzoomed_square_dimension;
}

const extract_machine_drawing_data = (item_machine_list) => {
    return {
        height: convert_to_grid_size(
            item_machine_list.type.y_dimension
        ),
        width: convert_to_grid_size(
            item_machine_list.type.x_dimension
        ),
        top: convert_to_grid_size(
            item_machine_list.y_position
        ) + 10, // offset of grid
        left: convert_to_grid_size(
            item_machine_list.x_position
        ) + 10, // offset of grid
        type: DrawingShape.Machine.name,
        rotation: item_machine_list.rotation,
        id: item_machine_list.id,
        name: item_machine_list.name,
        operator: item_machine_list.assigned_operator
    }
}

const set_current_result = (num) => {
    let index = num - 1;
    result_stats.value = results.value.at(index);
    result_machine_list.value = [];
    for (const machine of result_stats.value.machines) {
        result_machine_list.value.push(
            extract_machine_drawing_data(machine)
        );
    }
    areasStore.machines = Array.from(result_machine_list.value);
}

const incr = () => {
    number.value = number.value == total.value ? 1 : number.value + 1;
    set_current_result(number.value);
}

const decr = () => {
    number.value = number.value == 1 ? total.value : number.value - 1;
    set_current_result(number.value);
}

const restart = async () => {
    await get_request('new');
    const areasStore = useAreasStore();
    const processesStore = useProcessesStore();
    const machinesStore = useMachinesStore();
    const settingsStore = useSettingsStore();

    areasStore.reset();
    processesStore.reset();
    machinesStore.reset();
    settingsStore.reset();

    const planningStore = usePlanningStore();
    planningStore.setState(PlanningState.Areas);
    router.push('/');
}

onMounted(() => {
    get_results();
})
</script>

<template>
    <div class="expand">
        <div class="view-content">
            <div class="view-data">
                <div class="view-data-header">
                    <h1 v-if="result_id != undefined">Optimierungslauf {{ result_id }}</h1>
                    <h1 v-else>{{ title }}</h1>

                    <IconButton
                        text="Neuen Durchlauf starten"
                        @click="restart">
                        <IconPlus />
                    </IconButton>
                </div>
                <!-- Main content -->
                <ResultStatDisplay 
                    :number="number"
                    :total="total"
                    :stats="stats"
                    @incr="incr"
                    @decr="decr" />
                <MachineList
                    :machines="result_machine_list"
                    width="100%" />
            </div>
        </div>
        <div class="side-content">
            <div class="zoom-container">
                <ZoomDisplay />
            </div>
            <DrawingArea 
                :only-machines-movable="true" />
        </div>
    </div>
</template>

<style scoped>
.expand {
	width: 100%;
    height: 100%;
    display: inline-flex;
    overflow: hidden;
}

.view-content {
    width: fit-content;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-block: var(--site-margin-tb);
    padding-inline: var(--site-margin-lr);
    border-right: 1px solid var(--color-border);
    background-color: var(--color-background);
}

.view-data {
    display: flex;
    flex-direction: column;
    gap:  calc(var(--input-height) + var(--tool-area-padding));;
}

.view-data-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    background-color: var(--color-background);
}

.view-data-header > h1 {
    width: 100%;
    line-height: 1rem;
    padding: var(--tool-area-padding) 1.5rem calc(var(--tool-area-padding) - 1px) 1.5rem;
    border: 1px solid var(--color-border);
    border-right: none;
    font-size: var(--tool-area-height);
    font-weight: 500;
}

.view-data-header > p {
    line-height: 1;
    font-size: 0.8rem;
}

.side-content {
    width: 100%;
    height: 100%;
    position: relative;
}

.zoom-container {
    position: absolute;
    z-index: 3;
    top: var(--site-margin-tb);
    left: var(--site-margin-lr);
}
</style>