<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { usePlanningStore } from "../../../../store/store";
import PlanningInputColumn from "./PlanningInputColumn.vue";

const store = usePlanningStore();
const processOrder = ref([]);
const inputColumns = store.processOrderInputColumns;

const addProcess = () => {
  processOrder.value.push({
    order: processOrder.value.length + 1,
    technology: "",
    machineTime: null,
    manualTime: null
  });
};

const removeProcess = () => {
  processOrder.value.pop();
};

onMounted(() => {
  processOrder.value = store.processOrder;
  console.log(processOrder.value);
});

onUnmounted(() => {
  store.processOrder = processOrder.value;
});
</script>

<template>
  <div class="content">
    <PlanningInputColumn v-for="item in inputColumns" :key="item.id" :title="item.title" :type="item.type"
      :list="processOrder" :value="item.value" :selectList="item.selectList" :placeholder="item.placeholder"
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