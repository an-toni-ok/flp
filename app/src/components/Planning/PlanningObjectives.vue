<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useObjectiveStore } from "../../../store/objectives";
import PlanningInputColumn from "./PlanningInputColumn.vue";

const store = useObjectiveStore();
const objectives = ref([]);
const targetCycleTime = ref([{ value: null }]);
const hourlyOperatorCost = ref([{ value: null }]);
const inputColumns = store.objectiveInputColumns;

onMounted(() => {
    objectives.value = store.objectives;
    targetCycleTime.value[0].value = store.targetCycleTime;
    hourlyOperatorCost.value[0].value = store.hourlyOperatorCost;
});

onUnmounted(() => {
    store.objectives = objectives.value;
    store.targetCycleTime = targetCycleTime.value[0].value;
    store.hourlyOperatorCost = hourlyOperatorCost.value[0].value;
});
</script>

<template>
    <div class="content">
        <div class="row">
            <PlanningInputColumn v-for="item in inputColumns" :key="item.id" :title="item.title" :type="item.type"
                :object="objectives" :value="item.value">
            </PlanningInputColumn>
        </div>
        <div class="row">
            <div class="column">
                <h2 class="headline">Zielzykluszeit</h2>
                <PlanningInputColumn title="" type="inputNumber" :list="targetCycleTime" value="value" unit="s"
                    placeholder="10 s">
                </PlanningInputColumn>
            </div>
        </div>
        <div class="row">
            <div class="column">
                <h2 class="headline">Lohnkosten pro Stunde pro Werker</h2>
                <PlanningInputColumn title="" type="inputCurrency" :list="hourlyOperatorCost" value="value"
                    placeholder="35 €">
                </PlanningInputColumn>
            </div>
        </div>
    </div>
</template>

<style scoped>
.content,
.column {
    flex-direction: column;
}

.column {
    display: flex;
    align-content: flex-start;
}
</style>