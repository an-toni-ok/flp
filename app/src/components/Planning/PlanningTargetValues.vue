<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { usePlanningStore } from "../../../../store/store";
import PlanningInputColumn from "./PlanningInputColumn.vue";

const store = usePlanningStore();
const targetValues = ref([]);
const inputColumns = store.targetValueInputColumns;

onMounted(() => {
    targetValues.value = store.targetValues;
});

onUnmounted(() => {
    store.targetValues = targetValues.value;
});
</script>

<template>
    <div class="content">
        <PlanningInputColumn v-for="item in inputColumns" :key="item.id" :title="item.title" :type="item.type"
            :object="targetValues" :value="item.value">
        </PlanningInputColumn>
    </div>
</template>

<style scoped></style>