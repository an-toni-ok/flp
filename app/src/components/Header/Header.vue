<script setup>
import HeaderTitle from "./HeaderTitle.vue";
import HeaderLogo from "./HeaderLogo.vue";
import { useHeaderStore } from "../../../store/header";

const store = useHeaderStore();
</script>

<template>
  <div
    class="header"
    :style="{ height: store.headerHeight }"
  >
    <HeaderTitle></HeaderTitle>
    <HeaderLogo></HeaderLogo>
  </div>
</template>

<style>
:root {
  --header-bg-color: white;
}
</style>

<style scoped>
.header {
  color: #f30147;
  background-color: var(--header-bg-color);

  width: 100%;

  float: left;
  position: fixed;
  z-index: 4;
  top: 0;
  left: 0;

  transition: 0.3s ease;

  display: flex;
  align-items: center;
  vertical-align: middle;

  border: solid;
  border-width: 2px;
  border-color: black;
}
</style>