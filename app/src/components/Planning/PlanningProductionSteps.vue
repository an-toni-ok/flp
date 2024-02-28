<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useTechnologyStore } from "../../../store/technologies";
import { useProductionStepStore } from "../../../store/productionSteps";
import PlanningInputColumn from "./PlanningInputColumn.vue";

const store = useProductionStepStore();
const productionSteps = ref([]);
const inputColumns = store.productionStepInputColumns;
const technologies = useTechnologyStore().names;

const addProcess = () => {
  productionSteps.value.push({
    order: productionSteps.value.length + 1,
    technology: "",
    machineTime: null,
    manualTime: null
  });
};

const removeProcess = () => {
  productionSteps.value.pop();
};

onMounted(() => {
  productionSteps.value = store.productionSteps;
});

onUnmounted(() => {
  store.productionSteps = productionSteps.value;
});
</script>

<template>
  <div class="content">
    <PlanningInputColumn v-for="item in inputColumns" :key="item.id" :title="item.title" :type="item.type"
      :list="productionSteps" :value="item.value" :selectList="technologies" :placeholder="item.placeholder"
      :unit="item.unit" :min="item.min" :max="item.max" @add="addProcess" @remove="removeProcess">
    </PlanningInputColumn>
  </div>
</template>

<style>
.input-text-field {
  width: 7.2em;
}
</style>

<style scoped></style>