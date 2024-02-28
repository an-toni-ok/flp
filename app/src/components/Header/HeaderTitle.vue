<script setup>
import { useHeaderStore } from "../../../store/header";

const store = useHeaderStore();
</script>

<template>
  <div class="title">
    <h1>
      <p :style="{ width: store.sidebarWidth, 'margin-left': store.headerMarginLeft }">Layoutoptimierung für Produktionslinien</p>
    </h1>
  </div>
</template>

<style scoped>
.title {
  width: 90%;
  line-height: 1;
  display: inline-block;
  vertical-align: middle;
}

.title h1 p {
  font-size: 1em;
  font-weight: 400;
  text-align: left;
  padding-left: 40px;
}
</style>