<script setup>
import { onMounted, ref } from 'vue';
import { useAreasStore } from '@/stores/areas';

import MachineList from '@/components/Result/MachineList.vue';
import ResultsDisplay from '@/components/Result/ResultsDisplay.vue'
import DrawingArea from '@/components/DrawingArea.vue';
import { DrawingShape, get_request } from '@/util';

const areasStore = useAreasStore();

// Slide information
const title = "Optimierungsergebnisse";
const number = ref(1);
const total = ref(3);

const result_machine_list = ref([]);
const result_stats = ref({})
const results = ref([])

const get_results = async () => {
    const optimize_result = await get_request('optimize');
    const json_result = await optimize_result.json();
    results.value = json_result.output;
    total.value = results.value.length;
    set_current_result(number.value);
}

const convert_to_grid_size = (measurement) => {
    return measurement * 10 * areasStore.square_dimension
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
        ),
        left: convert_to_grid_size(
            item_machine_list.x_position
        ),
        type: DrawingShape.Machine.name,
        rotation: item_machine_list.rotation,
        id: item_machine_list.id
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
}

const incr = () => {
    number.value = number.value == total.value ? 1 : number.value + 1;
    set_current_result(number.value);
}

const decr = () => {
    number.value = number.value == 1 ? total.value : number.value - 1;
    set_current_result(number.value);
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
                    <h1>{{ title }}</h1>
                </div>
                <!-- Main content -->
                <ResultsDisplay 
                    v-model:number="number"
                    :total="total"
                    @incr="incr"
                    @decr="decr" />
                <MachineList />
            </div>
        </div>
        <div class="side-content">
            <DrawingArea 
                :only-machines-movable="true"
                :machines="result_machine_list" />
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
    border: 1px solid var(--color-border);
    gap: 2rem;
    padding: var(--tool-area-padding) 1.5rem;
}

.view-data-header > h1 {
    line-height: 1;
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
</style>