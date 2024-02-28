<script setup>
import Sidebar from "./components/Sidebar/Sidebar.vue";
import Header from "./components/Header/Header.vue";
import { useSidebarStore } from "../store/sidebar";
import { useHeaderStore } from "../store/header";

const sidebarStore = useSidebarStore();
const headerStore = useHeaderStore();
</script>

<template>
  <div class="app-container">
    <Header></Header>
    <Sidebar> </Sidebar>
    <div
      class="router-view-container"
      :style="{
        'margin-left': sidebarStore.sidebarWidth,
        'margin-top': headerStore.headerHeight,
      }"
    >
      <router-view v-slot="{ Component }">
        <KeepAlive>
          <component :is="Component"></component>
        </KeepAlive>
      </router-view>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
}

.router-view-container {
  width: 100%;

  transition: 0.3s ease;

  padding-top: 5px;
  padding-left: 40px;
}
</style>
