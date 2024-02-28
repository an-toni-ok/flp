<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useTechnologyStore } from "../../../store/technologies";
import PlanningInputColumn from "./PlanningInputColumn.vue";

const store = useTechnologyStore();
const technologies = ref([""]);
const inputColumns = store.technologyInputColumns;

const addTechnology = () => {
  technologies.value.push({
    technology: "",
  });
};

const removeTechnology = () => {
  technologies.value.pop();
};

onMounted(() => {
  technologies.value = store.technologies;
});

onUnmounted(() => {
  store.technologies = technologies.value;
});
</script>

<template>
  <div class="content">
    <PlanningInputColumn v-for="item in inputColumns" :key="item.id" :title="item.title" :type="item.type"
      :list="technologies" :value="item.value" :selectList="item.selectList" :placeholder="item.placeholder"
      :longTextfield=true @add="addTechnology" @remove="removeTechnology">
    </PlanningInputColumn>
  </div>
</template>

<style scoped></style>